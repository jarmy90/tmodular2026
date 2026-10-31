#property strict
#property version "4.000"
#property description "Explorer TM concurrente: AUT inmediato, maximo tres lecturas y reclasificacion live. No opera."

input string   InpSymbol                 = "";
input datetime InpInicio                 = D'2026.10.16 16:30:00';
input int      InpNumeroVelas            = 20;
input double   InpPlanoTolPuntos         = 1.00;
input double   InpMovimientoMinPuntos    = 3.00;
input double   InpGiroConsolidadoPuntos  = 6.00;
input double   InpAutExtraPuntos         = 0.25;
input int      InpMaxLecturas            = 3;
input string   InpPrefijo                = "TM_Live_Explorer_Concurrent_v40";

#define DIR_NONE 0
#define DIR_UP   1
#define DIR_DOWN -1

struct BarraTM
{
   bool activa;
   int indice;
   datetime inicio;
   double open,high,low,close;
   long ticks;
};

struct LecturaTM
{
   bool activa;
   int id;
   int padre;
   string tipo;
   string estado;
   string funcion;
   int direccion;
   int prioridad;
   int vela_inicio;
   int vela_ultimo;
   datetime tiempo_inicio;
   datetime tiempo_ultimo;
   double inicio;
   double extremo;
   double rango;
   double a_inicio;
   double a_final;
   double a_rango;
   double b_extremo;
   double b_pct;
   double nivel_aut;
   bool aut;
   bool candidato_uno;
   bool modulo;
   double modulo_rango;
   bool tt_pendiente;
   bool tt_confirmado;
   double objetivo_tt;
   bool correccion_activa;
   double correccion_extremo;
   bool reclasificada;
};

string g_symbol;
datetime g_fin;
BarraTM g_barra,g_prev;
LecturaTM g_l[3];
int g_seq=0;
int g_eventos=INVALID_HANDLE,g_estados=INVALID_HANDLE,g_resumen=INVALID_HANDLE;

bool g_swing_iniciado=false;
int g_swing_dir=DIR_NONE;
double g_swing_inicio=0.0,g_swing_extremo=0.0;
int g_swing_vela=0;

string DirTxt(const int d){ if(d==DIR_UP)return "ALCISTA"; if(d==DIR_DOWN)return "BAJISTA"; return "NINGUNA"; }
string SafeStem(string s){ StringReplace(s,".","-");StringReplace(s,":","-");StringReplace(s," ","_");return s; }
string SafeDetail(string s){ StringReplace(s,";"," -");StringReplace(s,"\r"," ");StringReplace(s,"\n"," ");return s; }

void Evento(const string tipo,const int lectura,const double precio,string detalle)
{
   detalle=SafeDetail(detalle);
   if(g_eventos!=INVALID_HANDLE)
      FileWrite(g_eventos,TimeToString(TimeCurrent(),TIME_DATE|TIME_SECONDS),(long)GetTickCount64(),g_barra.indice,lectura,tipo,DoubleToString(precio,_Digits),detalle);
}

void ResetLectura(LecturaTM &l){ ZeroMemory(l); }
int MaxLecturas(){ return MathMax(1,MathMin(3,InpMaxLecturas)); }
int SlotLibre(){ for(int i=0;i<MaxLecturas();i++) if(!g_l[i].activa) return i; return -1; }
int MenorPrioridad(){ int x=-1;for(int i=0;i<MaxLecturas();i++)if(g_l[i].activa&&(x<0||g_l[i].prioridad<g_l[x].prioridad))x=i;return x; }

void Archivar(const int idx,const string motivo,const double precio)
{
   if(idx<0||idx>=3||!g_l[idx].activa)return;
   Evento("LECTURA_ARCHIVADA",g_l[idx].id,precio,"tipo="+g_l[idx].tipo+" motivo="+motivo);
   ResetLectura(g_l[idx]);
}

int CrearLectura(const string tipo,const string funcion,const int dir,const double inicio,const double extremo,const int prioridad,const int padre,const double precio)
{
   int idx=SlotLibre();
   if(idx<0)
   {
      int menor=MenorPrioridad();
      if(menor>=0 && g_l[menor].prioridad<prioridad){ Archivar(menor,"prioridad superior",precio);idx=menor; }
   }
   if(idx<0){ Evento("LECTURA_SIN_SLOT",0,precio,"tipo="+tipo);return -1; }
   ResetLectura(g_l[idx]);
   g_l[idx].activa=true;g_l[idx].id=++g_seq;g_l[idx].padre=padre;g_l[idx].tipo=tipo;g_l[idx].estado="ACTIVA";g_l[idx].funcion=funcion;
   g_l[idx].direccion=dir;g_l[idx].prioridad=prioridad;g_l[idx].vela_inicio=g_barra.indice;g_l[idx].vela_ultimo=g_barra.indice;
   g_l[idx].tiempo_inicio=TimeCurrent();g_l[idx].tiempo_ultimo=TimeCurrent();g_l[idx].inicio=inicio;g_l[idx].extremo=extremo;g_l[idx].rango=MathAbs(extremo-inicio);
   Evento("LECTURA_CREADA",g_l[idx].id,precio,"tipo="+tipo+" funcion="+funcion+" padre="+IntegerToString(padre));
   return idx;
}

void EscribirEstado(const string motivo,const double precio)
{
   if(g_estados==INVALID_HANDLE)return;
   for(int i=0;i<MaxLecturas();i++)
   {
      LecturaTM l=g_l[i];
      FileWrite(g_estados,TimeToString(TimeCurrent(),TIME_DATE|TIME_SECONDS),g_barra.indice,motivo,i+1,l.activa?"SI":"NO",l.id,l.padre,l.tipo,l.estado,l.funcion,DirTxt(l.direccion),DoubleToString(precio,_Digits),l.vela_inicio,l.vela_ultimo,DoubleToString(l.inicio,_Digits),DoubleToString(l.extremo,_Digits),DoubleToString(l.rango,_Digits),DoubleToString(l.a_inicio,_Digits),DoubleToString(l.a_final,_Digits),DoubleToString(l.a_rango,_Digits),DoubleToString(l.b_extremo,_Digits),DoubleToString(l.b_pct,2),DoubleToString(l.nivel_aut,_Digits),l.aut?"SI":"NO",l.candidato_uno?"SI":"NO",l.modulo?"SI":"NO",DoubleToString(l.modulo_rango,_Digits),l.tt_pendiente?"SI":"NO",l.tt_confirmado?"SI":"NO",DoubleToString(l.objetivo_tt,_Digits),l.reclasificada?"SI":"NO");
   }
}

void CerrarBarra()
{
   if(!g_barra.activa)return;
   const double cuerpo=g_barra.close-g_barra.open;
   if(g_resumen!=INVALID_HANDLE)
      FileWrite(g_resumen,g_barra.indice,TimeToString(g_barra.inicio,TIME_DATE|TIME_MINUTES),DoubleToString(g_barra.open,_Digits),DoubleToString(g_barra.high,_Digits),DoubleToString(g_barra.low,_Digits),DoubleToString(g_barra.close,_Digits),DirTxt(cuerpo>=0?DIR_UP:DIR_DOWN),DoubleToString(MathAbs(cuerpo),_Digits),DoubleToString(g_barra.high-g_barra.low,_Digits));
   EscribirEstado("CIERRE_VELA",g_barra.close);
   g_prev=g_barra;
}

void NuevaBarra(const datetime inicio,const double precio)
{
   CerrarBarra();
   ZeroMemory(g_barra);g_barra.activa=true;g_barra.indice=(int)((inicio-InpInicio)/60)+1;g_barra.inicio=inicio;g_barra.open=precio;g_barra.high=precio;g_barra.low=precio;g_barra.close=precio;g_barra.ticks=1;
   Evento("NUEVA_VELA",0,precio,"indice="+IntegerToString(g_barra.indice));
   if(g_prev.activa)
   {
      double dif=precio-g_prev.close;
      if(MathAbs(dif)<=InpPlanoTolPuntos) Evento("SALIDA_PLANO",0,precio,"dif="+DoubleToString(dif,_Digits));
      else Evento("GAP",0,precio,"dif="+DoubleToString(dif,_Digits));
   }
}

void AbrirAUTDesdeMovimiento(const int dir,const double inicio,const double extremo,const double precio)
{
   int origen=CrearLectura("AUT_ORIGEN","TT_PRINCIPAL_O_PENDIENTE",dir,inicio,extremo,500,0,precio);
   int padre=(origen>=0?g_l[origen].id:0);
   if(origen>=0){ g_l[origen].aut=true;g_l[origen].estado="AUT_CONFIRMADO"; }
   int local=CrearLectura("UNO_CANDIDATO_AUT","POSIBLE_1_LOCAL",dir,inicio,extremo,350,padre,precio);
   if(local>=0){ g_l[local].aut=true;g_l[local].candidato_uno=true;g_l[local].estado="EN_OBSERVACION"; }
   Evento("AUT_BIFURCACION",padre,precio,"AUT inmediato - lectura origen y posible 1 local quedan en paralelo");
}

void EvaluarAUT(LecturaTM &l,const double precio)
{
   if(!l.activa || l.aut || l.a_rango<=0.0)return;
   double rec=MathAbs(precio-l.a_final);
   l.b_pct=100.0*rec/l.a_rango;
   l.b_extremo=precio;
   l.nivel_aut=(l.direccion==DIR_UP?l.a_final+1.27*l.a_rango+InpAutExtraPuntos:l.a_final-1.27*l.a_rango-InpAutExtraPuntos);
   bool toca=(l.direccion==DIR_UP?precio>=l.nivel_aut:precio<=l.nivel_aut);
   if(toca)
   {
      l.aut=true;l.estado="AUT_CONFIRMADO";
      Evento("AUT_CONFIRMADO",l.id,precio,"B%="+DoubleToString(l.b_pct,2));
      AbrirAUTDesdeMovimiento(l.direccion,l.a_final,precio,precio);
   }
}

void ActualizarLecturas(const double precio)
{
   for(int i=0;i<MaxLecturas();i++)
   {
      if(!g_l[i].activa)continue;
      bool ext=(g_l[i].direccion==DIR_UP?precio>g_l[i].extremo:precio<g_l[i].extremo);
      if(ext){g_l[i].extremo=precio;g_l[i].rango=MathAbs(precio-g_l[i].inicio);g_l[i].vela_ultimo=g_barra.indice;g_l[i].tiempo_ultimo=TimeCurrent();}
      if(g_l[i].tt_pendiente&&g_l[i].modulo)
      {
         bool tt=(g_l[i].direccion==DIR_UP?precio>=g_l[i].objetivo_tt:precio<=g_l[i].objetivo_tt);
         if(tt){g_l[i].tt_pendiente=false;g_l[i].tt_confirmado=true;g_l[i].estado="TT_CONFIRMADO";g_l[i].prioridad=550;Evento("TT_CONFIRMADO",g_l[i].id,precio,"objetivo alcanzado");}
      }
      EvaluarAUT(g_l[i],precio);
   }
}

void EvaluarCorreccion(const double precio)
{
   for(int i=0;i<MaxLecturas();i++)
   {
      if(!g_l[i].activa||!g_l[i].candidato_uno||g_l[i].reclasificada)continue;
      double corr=MathAbs(precio-g_l[i].extremo);
      if(g_barra.indice<=g_l[i].vela_inicio||corr<InpGiroConsolidadoPuntos)continue;
      g_l[i].reclasificada=true;g_l[i].estado="RECLASIFICADA";g_l[i].funcion="UNO_EN_REVISION";
      Evento("LECTURA_RECLASIFICADA",g_l[i].id,precio,"correccion="+DoubleToString(corr,_Digits));
      int m=CrearLectura("MODULO_CANDIDATO","MODULO_O_UNO_COMPUESTO",-g_l[i].direccion,g_l[i].inicio,g_l[i].extremo,425,g_l[i].id,precio);
      if(m>=0)
      {
         g_l[m].modulo=true;g_l[m].modulo_rango=MathAbs(g_l[m].extremo-g_l[m].inicio);g_l[m].a_inicio=g_l[m].extremo;g_l[m].a_final=precio;g_l[m].a_rango=MathAbs(precio-g_l[m].a_inicio);g_l[m].estado="A_GRANDE_CANDIDATA";
         Evento("A_GRANDE_CANDIDATA",g_l[m].id,precio,"velas previas en revision como modulo o 1 compuesto");
      }
   }
}

void ActualizarSwing(const double precio)
{
   if(!g_swing_iniciado){g_swing_iniciado=true;g_swing_inicio=precio;g_swing_extremo=precio;g_swing_vela=g_barra.indice;return;}
   if(g_swing_dir==DIR_NONE)
   {
      if(precio>=g_swing_extremo+InpMovimientoMinPuntos){g_swing_dir=DIR_UP;g_swing_extremo=precio;}
      else if(precio<=g_swing_extremo-InpMovimientoMinPuntos){g_swing_dir=DIR_DOWN;g_swing_extremo=precio;}
      return;
   }
   bool ext=(g_swing_dir==DIR_UP?precio>g_swing_extremo:precio<g_swing_extremo);
   if(ext){g_swing_extremo=precio;return;}
   double giro=MathAbs(precio-g_swing_extremo);
   if(giro<InpGiroConsolidadoPuntos)return;
   int idx=CrearLectura("MOVIMIENTO_BASE","UNO_O_A_CANDIDATO",g_swing_dir,g_swing_inicio,g_swing_extremo,250,0,precio);
   if(idx>=0)
   {
      g_l[idx].a_inicio=g_swing_extremo;g_l[idx].a_final=precio;g_l[idx].a_rango=giro;
      Evento("GIRO_CONSOLIDADO",g_l[idx].id,precio,"movimiento base registrado");
   }
   g_swing_inicio=g_swing_extremo;g_swing_dir=-g_swing_dir;g_swing_extremo=precio;g_swing_vela=g_barra.indice;
}

bool AbrirArchivos()
{
   string stamp=SafeStem(g_symbol+"_"+TimeToString(InpInicio,TIME_DATE|TIME_MINUTES));
   g_eventos=FileOpen(InpPrefijo+"_eventos_"+stamp+".csv",FILE_WRITE|FILE_CSV|FILE_ANSI|FILE_COMMON,';');
   g_estados=FileOpen(InpPrefijo+"_estados_"+stamp+".csv",FILE_WRITE|FILE_CSV|FILE_ANSI|FILE_COMMON,';');
   g_resumen=FileOpen(InpPrefijo+"_resumen_"+stamp+".csv",FILE_WRITE|FILE_CSV|FILE_ANSI|FILE_COMMON,';');
   if(g_eventos==INVALID_HANDLE||g_estados==INVALID_HANDLE||g_resumen==INVALID_HANDLE)return false;
   FileWrite(g_eventos,"time","time_msc","vela","lectura","evento","precio","detalle");
   FileWrite(g_estados,"time","vela","motivo","slot","activa","id","padre","tipo","estado","funcion","direccion","precio","vela_inicio","vela_ultimo","inicio","extremo","rango","a_inicio","a_final","a_rango","b_extremo","b_pct","nivel_aut","aut","candidato_uno","modulo","modulo_rango","tt_pendiente","tt_confirmado","objetivo_tt","reclasificada");
   FileWrite(g_resumen,"vela","inicio","open","high","low","close","direccion","cuerpo","rango");
   return true;
}

int OnInit()
{
   g_symbol=(InpSymbol==""?_Symbol:InpSymbol);g_fin=InpInicio+InpNumeroVelas*60;ZeroMemory(g_barra);ZeroMemory(g_prev);for(int i=0;i<3;i++)ResetLectura(g_l[i]);
   if(!AbrirArchivos())return INIT_FAILED;
   Print("TM Live Explorer Concurrent v4.000 iniciado");return INIT_SUCCEEDED;
}
void OnDeinit(const int reason){CerrarBarra();if(g_eventos!=INVALID_HANDLE)FileClose(g_eventos);if(g_estados!=INVALID_HANDLE)FileClose(g_estados);if(g_resumen!=INVALID_HANDLE)FileClose(g_resumen);}
void OnTick()
{
   MqlTick tk;if(!SymbolInfoTick(g_symbol,tk))return;datetime tm=(datetime)tk.time;double precio=(tk.bid+tk.ask)/2.0;
   if(tm<InpInicio||tm>=g_fin)return;datetime bi=tm-(tm%60);if(!g_barra.activa||bi!=g_barra.inicio)NuevaBarra(bi,precio);
   if(precio>g_barra.high)g_barra.high=precio;if(precio<g_barra.low)g_barra.low=precio;g_barra.close=precio;g_barra.ticks++;
   ActualizarSwing(precio);ActualizarLecturas(precio);EvaluarCorreccion(precio);
}
