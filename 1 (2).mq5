#property strict
#property version   "3.100"
#property description "Lector TM generico live, maximo dos escenarios, sin secuencia esperada ni conocimiento futuro. No opera."

input string   InpSymbol              = "";
input datetime InpInicio              = D'2026.10.16 16:30:00';
input int      InpNumeroVelas         = 10;
input double   InpPlanoTolPuntos      = 1.00;
input double   InpMovimientoMinPuntos = 3.00;
input double   InpGiroConsolidadoPuntos = 6.00; // Confirma fin de A/B/C, evita microretrocesos
input double   InpAutExtraPuntos      = 0.025;
input bool     InpExigirModuloParaTT   = true;
input bool     InpProtegerLecturaActiva = true;
input bool     InpLogEventos          = true;
input string   InpPrefijo             = "TM_Live_Reader_Generic_v31_BEX";

#define DIR_NONE  0
#define DIR_UP    1
#define DIR_DOWN -1
#define MAX_ESCENARIOS 2

struct BarraTM
{
   int indice;
   datetime inicio;
   double open;
   double high;
   double low;
   double close;
   long ticks;
   int direccion;
   double cuerpo;
   double rango;
};

struct ObservadorTM
{
   bool activo;
   bool promovido;
   int id;
   int direccion;
   string origen;
   string estado;
   datetime creado;
   int vela_creado;
   double inicio;
   double extremo;
   double rango;
   double retroceso_max;
};

struct EscenarioTM
{
   int id;
   bool activo;
   string fase;
   string origen;
   int direccion;
   datetime creado;

   bool primero;
   double uno_inicio;
   double uno_extremo;
   double uno_rango;
   int uno_vela;

   bool uno_en_formacion;
   bool uno_cerrado;
   bool uno_giro_candidato;
   double uno_giro_inicio;
   double uno_giro_extremo;
   double uno_retroceso_max;

   bool posible_dos;
   bool dos;
   double dos_inicio;
   double dos_extremo;
   double dos_rango;
   int dos_vela;

   bool posible_tres;
   bool tres;
   bool tres_fallido;
   bool tres_habilitado;
   int tres_desde_vela;
   double tres_retroceso_max;
   double tres_retroceso_pct;

   bool modulo;
   double modulo_min;
   double modulo_max;
   double modulo_rango;
   double modulo_estructural_rango;
   int modulo_desde;
   int modulo_hasta;

   bool a_activa;
   bool a_confirmada;
   int a_direccion;
   double a_inicio;
   double a_extremo;
   double a_rango;
   datetime a_t_inicio;
   datetime a_t_extremo;

   bool b_candidata;
   bool b_pendiente;
   bool b_confirmada;
   bool b_excesiva;
   bool b_excesiva_emitida;
   int b_direccion;
   double b_extremo;
   double b_pct;
   double nivel_b100;
   double nivel_b127;

   bool aut_activo;
   double nivel_aut;
   double precio_aut;
   datetime tiempo_aut;

   bool tt_pendiente;
   bool tt_confirmado;
   bool tt_fallido;
   double objetivo_tt;
   double tt_pct;

   bool c_candidata;
   bool c_activa;
   int c_direccion;
   double c_inicio;
   double c_extremo;
   double c_retroceso_max;
   bool cut_confirmado;

   bool nuevo_uno;
   int nuevo_uno_direccion;
   double nuevo_uno_inicio;
   double nuevo_uno_extremo;
   string nuevo_uno_origen;

   bool ft_candidato;
   bool ft_confirmado;
};

string g_symbol;
datetime g_fin;
BarraTM g_barra;
BarraTM g_prev;
bool g_hay_prev=false;
BarraTM g_historial[64];
int g_historial_total=0;
EscenarioTM g_e1,g_e2;
ObservadorTM g_observador;
int g_observador_seq=0;
int g_eventos=INVALID_HANDLE;
int g_estados=INVALID_HANDLE;
int g_resumen=INVALID_HANDLE;
bool g_terminado=false;

string DirTxt(const int d)
{
   if(d==DIR_UP) return "ALCISTA";
   if(d==DIR_DOWN) return "BAJISTA";
   return "NINGUNA";
}

string SafeStem(string s)
{
   StringReplace(s,".","-");
   StringReplace(s,":","-");
   StringReplace(s," ","_");
   StringReplace(s,"/","-");
   StringReplace(s,"\\","-");
   return s;
}

void ResetBarra(BarraTM &b,const int indice,const datetime inicio,const double precio)
{
   ZeroMemory(b);
   b.indice=indice;
   b.inicio=inicio;
   b.open=precio;
   b.high=precio;
   b.low=precio;
   b.close=precio;
}

void ResetEscenario(EscenarioTM &e,const int id)
{
   ZeroMemory(e);
   e.id=id;
   e.fase="VACIO";
}

void Evento(const string tipo,const int escenario,const double precio,const string detalle)
{
   string detalle_seguro=detalle;
   StringReplace(detalle_seguro,";"," -");
   StringReplace(detalle_seguro,"\r"," ");
   StringReplace(detalle_seguro,"\n"," ");
   if(g_eventos!=INVALID_HANDLE)
      FileWrite(g_eventos,
                TimeToString(TimeCurrent(),TIME_DATE|TIME_SECONDS),
                (long)TimeCurrent()*1000,
                g_barra.indice,
                escenario,
                tipo,
                DoubleToString(precio,_Digits),
                detalle_seguro,
                g_e1.fase,
                g_e2.fase);

   if(InpLogEventos)
      PrintFormat("TM | %s | V=%d | E=%d | %.*f | %s",
                  tipo,g_barra.indice,escenario,_Digits,precio,detalle_seguro);
}

void SnapshotUno(const EscenarioTM &e,const string motivo,const double precio)
{
   if(g_estados==INVALID_HANDLE) return;

   FileWrite(g_estados,
             TimeToString(TimeCurrent(),TIME_DATE|TIME_SECONDS),
             g_barra.indice,motivo,e.id,e.activo?"SI":"NO",e.fase,e.origen,
             DirTxt(e.direccion),DoubleToString(precio,_Digits),
             e.primero?"SI":"NO",e.uno_en_formacion?"SI":"NO",e.uno_cerrado?"SI":"NO",e.uno_giro_candidato?"SI":"NO",DoubleToString(e.uno_inicio,_Digits),DoubleToString(e.uno_extremo,_Digits),DoubleToString(e.uno_rango,_Digits),
             e.posible_dos?"SI":"NO",e.dos?"SI":"NO",DoubleToString(e.dos_rango,_Digits),
             e.posible_tres?"SI":"NO",e.tres?"SI":"NO",e.tres_fallido?"SI":"NO",DoubleToString(e.tres_retroceso_pct,2),
             e.modulo?"SI":"NO",DoubleToString(e.modulo_min,_Digits),DoubleToString(e.modulo_max,_Digits),DoubleToString(e.modulo_rango,_Digits),
             e.a_activa?"SI":"NO",DirTxt(e.a_direccion),DoubleToString(e.a_inicio,_Digits),DoubleToString(e.a_extremo,_Digits),DoubleToString(e.a_rango,_Digits),
             e.b_candidata?"SI":"NO",e.b_pendiente?"SI":"NO",e.b_confirmada?"SI":"NO",e.b_excesiva?"SI":"NO",DoubleToString(e.b_pct,2),DoubleToString(e.nivel_b100,_Digits),DoubleToString(e.nivel_b127,_Digits),
             e.aut_activo?"SI":"NO",DoubleToString(e.nivel_aut,_Digits),DoubleToString(e.precio_aut,_Digits),
             e.tt_pendiente?"SI":"NO",e.tt_confirmado?"SI":"NO",DoubleToString(e.objetivo_tt,_Digits),DoubleToString(e.tt_pct,2),
             e.c_candidata?"SI":"NO",e.c_activa?"SI":"NO",DirTxt(e.c_direccion),DoubleToString(e.c_extremo,_Digits),e.cut_confirmado?"SI":"NO",
             e.nuevo_uno?"SI":"NO",DirTxt(e.nuevo_uno_direccion),e.nuevo_uno_origen,
             e.ft_candidato?"SI":"NO",e.ft_confirmado?"SI":"NO");
}

void Snapshot(const string motivo,const double precio)
{
   SnapshotUno(g_e1,motivo,precio);
   SnapshotUno(g_e2,motivo,precio);
}

void CerrarBarra(BarraTM &b)
{
   b.direccion=(b.close>b.open ? DIR_UP : (b.close<b.open ? DIR_DOWN : DIR_NONE));
   b.cuerpo=MathAbs(b.close-b.open);
   b.rango=b.high-b.low;
}

void CrearPrimero(EscenarioTM &e,const BarraTM &b,const string origen)
{
   ResetEscenario(e,e.id);
   e.activo=true;
   e.fase="PRIMERO_ACTIVO";
   e.origen=origen;
   e.direccion=b.direccion;
   e.creado=TimeCurrent();
   e.primero=true;
   e.uno_en_formacion=false;
   e.uno_cerrado=true;
   e.uno_inicio=b.open;
   e.uno_extremo=b.close;
   e.uno_rango=b.cuerpo;
   e.uno_vela=b.indice;
   Evento("NUEVO_1",e.id,b.close,"direccion="+DirTxt(e.direccion)+" rango="+DoubleToString(e.uno_rango,_Digits));
}

void ActivarPosibleDos(EscenarioTM &e,const BarraTM &prev,const BarraTM &cur)
{
   if(!e.activo || !e.primero || !e.uno_cerrado || e.uno_en_formacion || e.dos) return;
   if(InpProtegerLecturaActiva && (e.a_activa || e.b_candidata || e.b_pendiente || e.b_confirmada || e.b_excesiva || e.aut_activo || e.tt_pendiente || e.c_candidata || e.c_activa)) return;

   const double dif=cur.open-prev.close;
   if(MathAbs(dif)>InpPlanoTolPuntos)
   {
      Evento("DOS_NO_ABIERTO_GAP",e.id,cur.open,"dif="+DoubleToString(dif,_Digits));
      return;
   }

   e.posible_dos=true;
   e.fase="POSIBLE_2";
   Evento("POSIBLE_2",e.id,cur.open,"salida en plano");
}

void ActualizarDos(EscenarioTM &e,const double precio)
{
   if(!e.activo || !e.posible_dos || e.dos) return;

   const double recorrido=(e.direccion==DIR_UP ? precio-g_barra.open : g_barra.open-precio);
   if(recorrido<=0) return;

   if(recorrido>=e.uno_rango)
   {
      e.dos=true;
      e.posible_dos=false;
      e.dos_inicio=g_barra.open;
      e.dos_extremo=precio;
      e.dos_rango=recorrido;
      e.dos_vela=g_barra.indice;
      e.posible_tres=true;
      e.tres_habilitado=false;
      e.tres_desde_vela=g_barra.indice;
      e.fase="POSIBLE_3";
      Evento("2_CONFIRMADO",e.id,precio,"rango2="+DoubleToString(recorrido,_Digits));
   }
}

bool ObtenerBarraHistorial(const int indice,BarraTM &salida)
{
   for(int i=0;i<g_historial_total;i++)
   {
      if(g_historial[i].indice==indice)
      {
         salida=g_historial[i];
         return true;
      }
   }
   return false;
}

void ActualizarTres(EscenarioTM &e,const double precio)
{
   if(!e.activo || !e.posible_tres || !e.dos || e.tres || e.tres_fallido) return;

   // El intento de 3 se observa dentro de la estela de 2, pero solo puede
   // resolverse despues de comenzar la vela siguiente a la que confirmo 2.
   if(g_barra.indice>e.tres_desde_vela)
      e.tres_habilitado=true;

   double retroceso=0.0;
   bool extremo_superado=false;

   if(e.direccion==DIR_DOWN)
   {
      extremo_superado=(precio<e.dos_extremo);
      if(extremo_superado)
      {
         e.dos_extremo=precio;
         e.tres_retroceso_max=0.0;
      }
      retroceso=precio-e.dos_extremo;
   }
   else
   {
      extremo_superado=(precio>e.dos_extremo);
      if(extremo_superado)
      {
         e.dos_extremo=precio;
         e.tres_retroceso_max=0.0;
      }
      retroceso=e.dos_extremo-precio;
   }

   if(retroceso>e.tres_retroceso_max) e.tres_retroceso_max=retroceso;
   e.tres_retroceso_pct=(e.dos_rango>0 ? 100.0*e.tres_retroceso_max/e.dos_rango : 0.0);

   if(!e.tres_habilitado) return;

   if(e.tres_retroceso_pct>50.0)
   {
      e.tres_fallido=true;
      e.posible_tres=false;
      e.fase="3_FALLIDO";
      Evento("3_FALLIDO",e.id,precio,"retroceso="+DoubleToString(e.tres_retroceso_pct,2)+"%");

      e.modulo=true;
      e.modulo_desde=e.uno_vela;
      e.modulo_hasta=e.dos_vela;
      // El modulo conserva dos medidas: estructural y High-Low completo.
      e.modulo_min=MathMin(MathMin(e.uno_inicio,e.uno_extremo),MathMin(e.dos_inicio,e.dos_extremo));
      e.modulo_max=MathMax(MathMax(e.uno_inicio,e.uno_extremo),MathMax(e.dos_inicio,e.dos_extremo));
      e.modulo_estructural_rango=e.modulo_max-e.modulo_min;
      BarraTM barra_uno;
      BarraTM barra_dos;
      const bool tiene_uno=ObtenerBarraHistorial(e.uno_vela,barra_uno);
      const bool tiene_dos=ObtenerBarraHistorial(e.dos_vela,barra_dos);
      if(tiene_uno && tiene_dos)
      {
         e.modulo_min=MathMin(barra_uno.low,barra_dos.low);
         e.modulo_max=MathMax(barra_uno.high,barra_dos.high);
      }
      e.modulo_rango=e.modulo_max-e.modulo_min;
      e.fase="MODULO_CONFIRMADO";
      Evento("MODULO_CONFIRMADO",e.id,precio,"rango="+DoubleToString(e.modulo_rango,_Digits));
      return;
   }

   if(extremo_superado)
   {
      e.tres=true;
      e.posible_tres=false;
      e.fase="3_CONFIRMADO";
      Evento("3_CONFIRMADO",e.id,precio,"continuacion valida despues de retroceso <=50%");
   }
}

void IniciarA(EscenarioTM &e,const double inicio,const double precio,const string origen)
{
   e.a_activa=true;
   e.a_confirmada=true;
   e.a_direccion=-e.direccion;
   e.a_inicio=inicio;
   e.a_extremo=precio;
   e.a_rango=MathAbs(precio-inicio);
   e.a_t_inicio=TimeCurrent();
   e.a_t_extremo=TimeCurrent();
   e.fase="A_ACTIVA";
   Evento("A_ACTIVA",e.id,precio,origen+" rango="+DoubleToString(e.a_rango,_Digits));
}

void ActualizarA(EscenarioTM &e,const double precio)
{
   if(!e.activo || !e.a_activa || e.b_confirmada) return;

   const bool nuevo_extremo_a=(e.a_direccion==DIR_UP ? precio>e.a_extremo : precio<e.a_extremo);
   if(nuevo_extremo_a)
   {
      if(e.b_candidata || e.b_pendiente)
      {
         e.b_candidata=false;
         e.b_pendiente=false;
         e.b_pct=0.0;
         Evento("B_CANDIDATA_CANCELADA",e.id,precio,"A crea nuevo extremo");
      }
      e.a_extremo=precio;
      e.a_rango=MathAbs(e.a_extremo-e.a_inicio);
      e.a_t_extremo=TimeCurrent();
      return;
   }

   const double giro=MathAbs(precio-e.a_extremo);
   const bool gira=(e.a_direccion==DIR_UP ? precio<e.a_extremo : precio>e.a_extremo);
   if(gira && !e.b_candidata && e.a_rango>=InpMovimientoMinPuntos && giro>=InpGiroConsolidadoPuntos)
   {
      e.b_candidata=true;
      e.b_pendiente=true;
      e.b_direccion=-e.a_direccion;
      e.b_extremo=precio;
      e.nivel_b100=e.a_inicio;
      e.nivel_b127=(e.b_direccion==DIR_UP ? e.a_extremo+1.27*e.a_rango : e.a_extremo-1.27*e.a_rango);
      e.nivel_aut=(e.b_direccion==DIR_UP ? e.nivel_b127+InpAutExtraPuntos : e.nivel_b127-InpAutExtraPuntos);
      e.fase="B_CANDIDATA";
      Evento("B_CANDIDATA",e.id,precio,"B100="+DoubleToString(e.nivel_b100,_Digits));
   }
}

void ResetObservador()
{
   ZeroMemory(g_observador);
   g_observador.estado="VACIO";
}

void CrearObservadorDesdeBExcesiva(const EscenarioTM &e,const double precio)
{
   if(g_observador.activo) return;
   ResetObservador();
   g_observador.activo=true;
   g_observador.id=++g_observador_seq;
   g_observador.direccion=e.b_direccion;
   g_observador.origen="B_EXCESIVA_E"+IntegerToString(e.id);
   g_observador.estado="NUEVO_1_CANDIDATO";
   g_observador.creado=TimeCurrent();
   g_observador.vela_creado=g_barra.indice;
   g_observador.inicio=e.a_extremo;
   g_observador.extremo=precio;
   g_observador.rango=MathAbs(precio-g_observador.inicio);
   Evento("OBSERVADOR_NUEVO_1",0,precio,"origen="+g_observador.origen+" rango="+DoubleToString(g_observador.rango,_Digits));
}

bool EscenarioPuedeRetirarse(const EscenarioTM &e)
{
   if(!e.activo) return true;
   if(e.tt_confirmado || e.cut_confirmado) return true;
   return false;
}

void PromoverObservador(const double precio)
{
   if(!g_observador.activo || g_observador.promovido) return;
   const double retroceso=MathAbs(precio-g_observador.extremo);
   if(retroceso<InpGiroConsolidadoPuntos) return;
   if(g_barra.indice<=g_observador.vela_creado) return;

   int destino=0;
   if(EscenarioPuedeRetirarse(g_e1)) destino=1;
   else if(EscenarioPuedeRetirarse(g_e2)) destino=2;
   if(destino==0)
   {
      Evento("OBSERVADOR_ESPERA",0,precio,"sin slot retirable");
      return;
   }

   EscenarioTM nuevo;
   ZeroMemory(nuevo);
   nuevo.id=destino;
   nuevo.activo=true;
   nuevo.fase="PRIMERO_CERRADO_A_ACTIVA";
   nuevo.origen=g_observador.origen;
   nuevo.direccion=g_observador.direccion;
   nuevo.primero=true;
   nuevo.uno_en_formacion=false;
   nuevo.uno_cerrado=true;
   nuevo.uno_inicio=g_observador.inicio;
   nuevo.uno_extremo=g_observador.extremo;
   nuevo.uno_rango=MathAbs(nuevo.uno_extremo-nuevo.uno_inicio);
   nuevo.uno_vela=g_observador.vela_creado;
   nuevo.a_activa=true;
   nuevo.a_confirmada=true;
   nuevo.a_direccion=-nuevo.direccion;
   nuevo.a_inicio=nuevo.uno_extremo;
   nuevo.a_extremo=precio;
   nuevo.a_rango=MathAbs(precio-nuevo.a_inicio);
   nuevo.a_t_inicio=TimeCurrent();
   nuevo.a_t_extremo=TimeCurrent();

   if(destino==1) g_e1=nuevo; else g_e2=nuevo;
   g_observador.promovido=true;
   g_observador.activo=false;
   Evento("OBSERVADOR_PROMOVIDO",destino,precio,"nuevo 1 cerrado y A activa");
}

void ActualizarObservador(const double precio)
{
   if(!g_observador.activo) return;
   const bool extiende=(g_observador.direccion==DIR_UP ? precio>g_observador.extremo : precio<g_observador.extremo);
   if(extiende)
   {
      g_observador.extremo=precio;
      g_observador.rango=MathAbs(g_observador.extremo-g_observador.inicio);
      g_observador.retroceso_max=0.0;
      return;
   }
   const double retroceso=MathAbs(precio-g_observador.extremo);
   if(retroceso>g_observador.retroceso_max) g_observador.retroceso_max=retroceso;
   PromoverObservador(precio);
}

void ActualizarB(EscenarioTM &e,const double precio)
{
   if(!e.activo || (!e.b_pendiente && !e.b_confirmada && !e.aut_activo && !e.tt_pendiente)) return;

   const bool extiende=(e.b_direccion==DIR_UP ? precio>e.b_extremo : precio<e.b_extremo);
   if(extiende) e.b_extremo=precio;

   const double recorrido=MathAbs(e.b_extremo-e.a_extremo);
   e.b_pct=(e.a_rango>0 ? 100.0*recorrido/e.a_rango : 0.0);
   const double limite_b_pct=(e.a_rango>0.0 ? 127.0+(InpAutExtraPuntos/e.a_rango*100.0) : 127.0);

   if(e.b_pct>limite_b_pct && !e.b_excesiva)
   {
      e.b_excesiva=true;
      e.b_excesiva_emitida=true;
      e.b_candidata=false;
      e.b_pendiente=false;
      e.b_confirmada=false;
      e.c_candidata=false;
      e.c_activa=false;
      e.aut_activo=false;
      e.tt_pendiente=false;
      e.fase="B_EXCESIVA";
      Evento("B_EXCESIVA",e.id,precio,"B%="+DoubleToString(e.b_pct,2)+" limite="+DoubleToString(limite_b_pct,2));
      CrearObservadorDesdeBExcesiva(e,precio);
      return;
   }

   if(e.b_excesiva) return;

   if(e.b_pendiente && e.b_pct>=100.0)
   {
      e.b_candidata=false;
      e.b_pendiente=false;
      e.b_confirmada=true;
      e.fase="B_CONFIRMADA";
      Evento("B_CONFIRMADA",e.id,precio,"pct="+DoubleToString(e.b_pct,2));
   }

   const bool toca_aut=(e.b_direccion==DIR_UP ? precio>=e.nivel_aut : precio<=e.nivel_aut);
   if(!e.aut_activo && toca_aut)
   {
      if(e.c_candidata || e.c_activa)
      {
         e.c_candidata=false;
         e.c_activa=false;
         Evento("C_CANCELADA",e.id,precio,"B alcanza AUT");
      }
      e.aut_activo=true;
      e.precio_aut=precio;
      e.tiempo_aut=TimeCurrent();
      const bool modulo_valido=(e.modulo && e.modulo_rango>0.0);
      if(!InpExigirModuloParaTT || modulo_valido)
      {
         e.tt_pendiente=true;
         e.objetivo_tt=(e.direccion==DIR_UP ? e.a_extremo+e.modulo_rango : e.a_extremo-e.modulo_rango);
         e.fase="AUT_TT_PENDIENTE";
         Evento("AUT_ACTIVO",e.id,precio,"objetivoTT="+DoubleToString(e.objetivo_tt,_Digits));
      }
      else
      {
         e.tt_pendiente=false;
         e.objetivo_tt=0.0;
         e.fase="AUT_SIN_TT";
         Evento("AUT_SIN_TT",e.id,precio,"AUT valido; TT bloqueado por falta de modulo");
      }
   }

   if(e.tt_pendiente && e.modulo && e.modulo_rango>0.0)
   {
      e.tt_pct=100.0*MathAbs(precio-e.a_extremo)/e.modulo_rango;
      const bool toca_tt=(e.direccion==DIR_UP ? precio>=e.objetivo_tt : precio<=e.objetivo_tt);
      if(toca_tt)
      {
         e.tt_pendiente=false;
         e.tt_confirmado=true;
         e.nuevo_uno=true;
         e.nuevo_uno_direccion=e.direccion;
         e.nuevo_uno_inicio=(e.precio_aut!=0.0 ? e.precio_aut : precio);
         e.nuevo_uno_extremo=precio;
         e.nuevo_uno_origen="TT";
         e.ft_candidato=true;
         e.fase="TT_CONFIRMADO_NUEVO_1";
         Evento("TT_CONFIRMADO",e.id,precio,"progreso="+DoubleToString(e.tt_pct,2));
      }
   }
}

void ActualizarC(EscenarioTM &e,const double precio)
{
   if(!e.activo || !e.b_confirmada || e.b_excesiva || e.aut_activo) return;

   const int dirC=e.a_direccion;
   const bool se_aleja_de_b=(dirC==DIR_UP ? precio>e.b_extremo : precio<e.b_extremo);
   const bool b_extiende=(e.b_direccion==DIR_UP ? precio>e.b_extremo : precio<e.b_extremo);

   if(b_extiende)
   {
      e.b_extremo=precio;
      if(e.c_candidata || e.c_activa)
      {
         e.c_candidata=false;
         e.c_activa=false;
         e.c_retroceso_max=0.0;
         Evento("C_CANCELADA",e.id,precio,"B crea nuevo extremo");
      }
      return;
   }

   if(se_aleja_de_b && !e.c_candidata && !e.c_activa)
   {
      e.c_candidata=true;
      e.c_direccion=dirC;
      e.c_inicio=e.b_extremo;
      e.c_extremo=precio;
      e.c_retroceso_max=MathAbs(precio-e.c_inicio);
      Evento("C_CANDIDATA",e.id,precio,"esperando movimiento consolidado");
   }

   if(e.c_candidata)
   {
      const bool extiende=(dirC==DIR_UP ? precio>e.c_extremo : precio<e.c_extremo);
      if(extiende) e.c_extremo=precio;
      e.c_retroceso_max=MathAbs(e.c_extremo-e.c_inicio);
      if(e.c_retroceso_max>=InpGiroConsolidadoPuntos)
      {
         e.c_candidata=false;
         e.c_activa=true;
         e.fase="C_ACTIVA";
         Evento("C_CONFIRMADA",e.id,precio,"movimiento contrario consolidado");
      }
   }

   if(!e.c_activa) return;

   const bool extiende=(dirC==DIR_UP ? precio>e.c_extremo : precio<e.c_extremo);
   if(extiende) e.c_extremo=precio;

   const bool superaA=(dirC==DIR_UP ? precio>e.a_extremo : precio<e.a_extremo);
   if(superaA && !e.cut_confirmado)
   {
      e.cut_confirmado=true;
      e.nuevo_uno=true;
      e.nuevo_uno_direccion=dirC;
      e.nuevo_uno_inicio=e.c_inicio;
      e.nuevo_uno_extremo=precio;
      e.nuevo_uno_origen="C_CUT";
      e.fase="CUT_NUEVO_1";
      Evento("CUT_CONFIRMADO",e.id,precio,"C=nuevo1; candidato A de lectura superior");
   }
}

void ActualizarUnoEnFormacion(EscenarioTM &e,const double precio)
{
   if(!e.activo || !e.uno_en_formacion || !e.primero) return;

   const bool extiende=(e.direccion==DIR_UP ? precio>e.uno_extremo : precio<e.uno_extremo);
   if(extiende)
   {
      if(e.uno_giro_candidato)
      {
         e.uno_giro_candidato=false;
         e.uno_retroceso_max=0.0;
         Evento("A_LOCAL_CANDIDATA_CANCELADA",e.id,precio,"nuevo 1 crea otro extremo");
      }
      e.uno_extremo=precio;
      e.uno_rango=MathAbs(e.uno_extremo-e.uno_inicio);
      return;
   }

   const double retroceso=MathAbs(precio-e.uno_extremo);
   if(retroceso>e.uno_retroceso_max) e.uno_retroceso_max=retroceso;

   if(!e.uno_giro_candidato && retroceso>=InpGiroConsolidadoPuntos)
   {
      e.uno_giro_candidato=true;
      e.uno_giro_inicio=e.uno_extremo;
      e.uno_giro_extremo=precio;
      Evento("A_LOCAL_CANDIDATA",e.id,precio,"esperando confirmacion sin nuevo extremo de 1");
   }

   if(e.uno_giro_candidato)
   {
      const int dirA=-e.direccion;
      const bool extiendeA=(dirA==DIR_UP ? precio>e.uno_giro_extremo : precio<e.uno_giro_extremo);
      if(extiendeA) e.uno_giro_extremo=precio;

      // La candidata solo puede cerrar 1 desde una vela posterior a su nacimiento.
      if(g_barra.indice>e.uno_vela && MathAbs(e.uno_giro_extremo-e.uno_giro_inicio)>=InpGiroConsolidadoPuntos)
      {
         e.uno_en_formacion=false;
         e.uno_cerrado=true;
         e.uno_giro_candidato=false;
         e.fase="PRIMERO_CERRADO_A_ACTIVA";
         Evento("NUEVO_1_CERRADO",e.id,e.uno_extremo,"rango="+DoubleToString(e.uno_rango,_Digits));
         IniciarA(e,e.uno_extremo,e.uno_giro_extremo,"A local confirmada");
      }
   }
}

void ProcesarEscenario(EscenarioTM &e,const double precio)
{
   if(!e.activo) return;

   ActualizarUnoEnFormacion(e,precio);
   ActualizarDos(e,precio);
   ActualizarTres(e,precio);

   if(e.modulo && !e.a_activa)
   {
      const double referencia=e.dos_extremo;
      const bool contrario=(e.direccion==DIR_DOWN ? precio>referencia : precio<referencia);
      if(contrario && MathAbs(precio-referencia)>=InpMovimientoMinPuntos)
         IniciarA(e,referencia,precio,"A del modulo");
   }

   ActualizarA(e,precio);
   ActualizarB(e,precio);
   ActualizarC(e,precio);
}

void RotarDespuesTT(EscenarioTM &principal,const double precio)
{
   if(!principal.tt_confirmado || !principal.nuevo_uno) return;
   if(g_e2.activo) return;

   ResetEscenario(g_e2,2);
   g_e2.activo=true;
   g_e2.fase="PRIMERO_ACTIVO";
   g_e2.origen="NUEVO_1_DESDE_TT";
   g_e2.direccion=principal.nuevo_uno_direccion;
   g_e2.primero=true;
   g_e2.uno_en_formacion=true;
   g_e2.uno_cerrado=false;
   g_e2.uno_inicio=principal.nuevo_uno_inicio;
   g_e2.uno_extremo=precio;
   g_e2.uno_rango=MathAbs(precio-g_e2.uno_inicio);
   g_e2.uno_vela=g_barra.indice;
   Evento("LECTURA_LOCAL_POST_TT",2,precio,"nuevo 1 local creado sin borrar lectura principal");
}

void ConfigurarLecturaSuperior(EscenarioTM &destino,const EscenarioTM &fuente,const double precio)
{
   const int id_destino=destino.id;
   ResetEscenario(destino,id_destino);
   destino.activo=true;
   destino.origen="C_COMO_A_SUPERIOR";
   destino.fase="A_SUPERIOR_ACTIVA";
   destino.direccion=-fuente.c_direccion;
   destino.modulo=true;
   destino.modulo_desde=MathMax(1,g_prev.indice-1);
   destino.modulo_hasta=g_prev.indice;
   destino.modulo_min=MathMin(g_prev.low,g_barra.low);
   destino.modulo_max=MathMax(g_prev.high,g_barra.high);
   destino.modulo_rango=destino.modulo_max-destino.modulo_min;
   destino.a_activa=true;
   destino.a_confirmada=true;
   destino.a_direccion=fuente.c_direccion;
   destino.a_inicio=fuente.c_inicio;
   destino.a_extremo=fuente.c_extremo;
   destino.a_rango=MathAbs(destino.a_extremo-destino.a_inicio);
   Evento("LECTURA_SUPERIOR_CREADA",destino.id,precio,"C reutilizada como A superior; lectura resuelta retirada si fue necesario");
}

void IntentarLecturaSuperior(const EscenarioTM &fuente,const double precio)
{
   if(!fuente.cut_confirmado || !g_hay_prev) return;

   if(fuente.id==1)
   {
      if(!g_e2.activo)
      {
         ConfigurarLecturaSuperior(g_e2,fuente,precio);
         return;
      }
      Evento("LECTURA_SUPERIOR_ESPERA",1,precio,"E2 ocupada; se mantiene candidato superior");
      return;
   }

   if(fuente.id==2)
   {
      // E1 puede retirarse cuando su TT ya esta resuelto. Se conserva el maximo de dos lecturas vivas.
      if(g_e1.tt_confirmado)
      {
         Evento("LECTURA_RESUELTA_RETIRADA",1,precio,"E1 TT confirmado; libera slot para lectura superior");
         ConfigurarLecturaSuperior(g_e1,fuente,precio);
         return;
      }
      Evento("LECTURA_SUPERIOR_ESPERA",2,precio,"E1 aun no es retirable");
   }
}

void CerrarActual()
{
   CerrarBarra(g_barra);

   if(g_resumen!=INVALID_HANDLE)
      FileWrite(g_resumen,g_barra.indice,TimeToString(g_barra.inicio,TIME_DATE|TIME_MINUTES),
                DoubleToString(g_barra.open,_Digits),DoubleToString(g_barra.high,_Digits),
                DoubleToString(g_barra.low,_Digits),DoubleToString(g_barra.close,_Digits),
                DirTxt(g_barra.direccion),DoubleToString(g_barra.cuerpo,_Digits),DoubleToString(g_barra.rango,_Digits),
                g_e1.fase,g_e2.fase);

   Evento("CIERRE_VELA",0,g_barra.close,"direccion="+DirTxt(g_barra.direccion));

   if(g_barra.indice==1 && !g_e1.activo && g_barra.direccion!=DIR_NONE && g_barra.cuerpo>=InpMovimientoMinPuntos)
      CrearPrimero(g_e1,g_barra,"PRIMERA_REFERENCIA_CONSOLIDADA");

   if(g_historial_total<64)
      g_historial[g_historial_total++]=g_barra;
   g_prev=g_barra;
   g_hay_prev=true;
   Snapshot("CIERRE_VELA",g_barra.close);
}

void NuevaBarra(const datetime inicio,const double precio)
{
   if(g_barra.indice>0) CerrarActual();

   const int indice=(int)((inicio-InpInicio)/60)+1;
   ResetBarra(g_barra,indice,inicio,precio);
   Evento("NUEVA_VELA",0,precio,"indice="+IntegerToString(indice));

   if(g_hay_prev)
   {
      const double dif=precio-g_prev.close;
      Evento(MathAbs(dif)<=InpPlanoTolPuntos ? "SALIDA_PLANO" : "GAP",
             0,precio,"dif="+DoubleToString(dif,_Digits));
      ActivarPosibleDos(g_e1,g_prev,g_barra);
      ActivarPosibleDos(g_e2,g_prev,g_barra);
   }

   Snapshot("NUEVA_VELA",precio);
}

void ProcesarTick(const MqlTick &tk)
{
   const double precio=tk.bid;
   const datetime inicio_barra=(datetime)(tk.time/60*60);

   if(g_barra.indice==0 || inicio_barra!=g_barra.inicio)
      NuevaBarra(inicio_barra,precio);

   if(g_barra.ticks==0) g_barra.open=precio;
   if(precio>g_barra.high) g_barra.high=precio;
   if(precio<g_barra.low) g_barra.low=precio;
   g_barra.close=precio;
   g_barra.ticks++;

   ProcesarEscenario(g_e1,precio);
   RotarDespuesTT(g_e1,precio);
   ProcesarEscenario(g_e2,precio);
   ActualizarObservador(precio);
   IntentarLecturaSuperior(g_e1,precio);
   IntentarLecturaSuperior(g_e2,precio);
}

bool AbrirArchivos()
{
   const string stamp=SafeStem(g_symbol+"_"+TimeToString(InpInicio,TIME_DATE|TIME_MINUTES));
   const string f1=InpPrefijo+"_eventos_"+stamp+".csv";
   const string f2=InpPrefijo+"_estados_"+stamp+".csv";
   const string f3=InpPrefijo+"_resumen_"+stamp+".csv";

   g_eventos=FileOpen(f1,FILE_WRITE|FILE_CSV|FILE_ANSI|FILE_COMMON,';');
   g_estados=FileOpen(f2,FILE_WRITE|FILE_CSV|FILE_ANSI|FILE_COMMON,';');
   g_resumen=FileOpen(f3,FILE_WRITE|FILE_CSV|FILE_ANSI|FILE_COMMON,';');
   if(g_eventos==INVALID_HANDLE || g_estados==INVALID_HANDLE || g_resumen==INVALID_HANDLE) return false;

   FileWrite(g_eventos,"time","time_msc","vela","escenario","evento","precio","detalle","fase_e1","fase_e2");
   FileWrite(g_estados,"time","vela","motivo","escenario","activo","fase","origen","direccion","precio",
             "primero","uno_en_formacion","uno_cerrado","uno_giro_candidato","uno_inicio","uno_extremo","uno_rango","posible2","dos","dos_rango","posible3","tres","tres_fallido","retroceso3_pct",
             "modulo","modulo_min","modulo_max","modulo_rango","a_activa","a_direccion","a_inicio","a_extremo","a_rango",
             "b_candidata","b_pendiente","b_confirmada","b_excesiva","b_pct","b100","b127","aut","nivel_aut","precio_aut","tt_pendiente","tt_confirmado","objetivo_tt","tt_pct",
             "c_candidata","c_activa","c_direccion","c_extremo","cut","nuevo1","nuevo1_direccion","nuevo1_origen","ft_candidato","ft_confirmado");
   FileWrite(g_resumen,"vela","inicio","open","high","low","close","direccion","cuerpo","rango","fase_e1","fase_e2");
   return true;
}

int OnInit()
{
   g_symbol=(InpSymbol=="" ? _Symbol : InpSymbol);
   g_fin=InpInicio+InpNumeroVelas*60;
   ZeroMemory(g_barra);
   ZeroMemory(g_prev);
   ResetEscenario(g_e1,1);
   ResetEscenario(g_e2,2);
   ResetObservador();

   if(!AbrirArchivos()) return INIT_FAILED;

   PrintFormat("TM Live Reader Generic v3.100 | %s | %s -> %s",
               g_symbol,
               TimeToString(InpInicio,TIME_DATE|TIME_SECONDS),
               TimeToString(g_fin,TIME_DATE|TIME_SECONDS));
   return INIT_SUCCEEDED;
}

void OnTick()
{
   if(g_terminado) return;

   MqlTick tk;
   if(!SymbolInfoTick(g_symbol,tk)) return;
   if(tk.time<InpInicio) return;

   if(tk.time>=g_fin)
   {
      if(g_barra.indice>0) CerrarActual();
      Evento("FIN_LECTURA",0,tk.bid,"periodo completado sin secuencia esperada");
      Snapshot("FIN",tk.bid);
      FileFlush(g_eventos);
      FileFlush(g_estados);
      FileFlush(g_resumen);
      g_terminado=true;
      Print("TM Live Reader Generic finalizado. Tres CSV en Terminal/Common/Files.");
      return;
   }

   ProcesarTick(tk);
}

void OnDeinit(const int reason)
{
   if(g_eventos!=INVALID_HANDLE) FileClose(g_eventos);
   if(g_estados!=INVALID_HANDLE) FileClose(g_estados);
   if(g_resumen!=INVALID_HANDLE) FileClose(g_resumen);
}
