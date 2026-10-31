PAQUETE TM OPENCODE MULTIAGENTE

1. NO borres C:\Users\profesor\.config\opencode.
2. Haz una copia de seguridad de esa carpeta.
3. Extrae la carpeta tm-explorer de este ZIP en la raiz real de tu proyecto.
   Debe quedar: TU_PROYECTO\AGENTS.md y TU_PROYECTO\.opencode\agents\...
4. Copia dentro del proyecto tus carpetas dossier, data, golden, src y tests.
5. Abre OpenCode desde la raiz del proyecto, no desde C:\Users\profesor\.config\opencode.
6. Inicia una sesion nueva y selecciona tm-orchestrator si no aparece automaticamente.
7. Prompt inicial recomendado:

Lee AGENTS.md. No escribas codigo. Audita la estructura y lanza en paralelo
@rules-analyst, @movement-reconstructor y @data-auditor. Despues sintetiza
hallazgos con @tm-reviewer. Devuelve agentes usados, evidencias, dudas y estado
del Gate Cero. No llames a @core-tm-engineer mientras el Gate Cero este cerrado.

NOTA SOBRE TU CONFIGURACION GLOBAL
El ZIP revisado contiene 10 perfiles configurados en opencode.json: build mas
nueve subagentes genericos. No son solo cuatro. Tambien contiene muchos prompts
y comandos ECC. No hace falta borrarlos. Los agentes TM de este paquete son
locales al proyecto y tienen nombres propios, por lo que no colisionan.

No copies node_modules del ZIP antiguo a cada proyecto. Se regenera con el
gestor de paquetes cuando sea necesario.
