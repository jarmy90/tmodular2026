from __future__ import annotations
import difflib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def diff(old:Path,new:Path,name:str,old_label:str,new_label:str)->None:
    text="".join(difflib.unified_diff(old.read_text(encoding="utf-8",errors="replace").splitlines(True),
        new.read_text(encoding="utf-8",errors="replace").splitlines(True),
        fromfile=old_label,tofile=new_label))
    (ROOT/name).write_text(text,encoding="utf-8",newline="\n")

diff(ROOT/"authority"/"TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_12.md",
     ROOT/"authority"/"TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_13_PROPUESTA_R2.md",
     "diff_v2_12_to_v2_13_R2.patch","v2.12/TM_ARBOL_ACTIVO.md","v2.13_R2/propuesta.md")
diff(ROOT/"authority"/"TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_13_PROPUESTA_R1.md",
     ROOT/"authority"/"TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_13_PROPUESTA_R2.md",
     "diff_v2_13_R1_to_R2.patch","v2.13_R1.md","v2.13_R2.md")
diff(ROOT.parent/"TM_CORE_v0752_R2_CANDIDATO"/"python"/"TM_CORE_PYTHON_v0752_CANONICAL.py",
     ROOT/"python"/"TM_CORE_PYTHON_v0752_CANONICAL.py",
     "diff_v0752_R2_to_R3.patch","v0.7.5.2-R2.py","v0.7.5.2-R3.py")
print("Created three unified diffs.")
