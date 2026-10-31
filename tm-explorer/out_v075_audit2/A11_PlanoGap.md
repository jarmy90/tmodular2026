# Regla de plano y GAP

La correccion confirmada por Javier exige: `|apertura - cierre anterior| < 0,25` es plano;
`0,25` exacto o superior no es plano. Por tanto no debe emitirse `GAP` para 0,10 o 0,20.

- Velas: `75`.
- GAP esperados: `62`; GAP observados: `74`.
- Falsos GAP: `12`; GAP omitidos: `0`.
- Velas conformes: `63/75`.

## Falsos GAP

- `16:16` gap `0.10` esperado `PLANO_NO_GAP` observado `GAP`
- `16:20` gap `-0.20` esperado `PLANO_NO_GAP` observado `GAP`
- `16:27` gap `0.20` esperado `PLANO_NO_GAP` observado `GAP`
- `16:39` gap `0.20` esperado `PLANO_NO_GAP` observado `GAP`
- `16:45` gap `0.10` esperado `PLANO_NO_GAP` observado `GAP`
- `17:04` gap `0.10` esperado `PLANO_NO_GAP` observado `GAP`
- `17:07` gap `-0.20` esperado `PLANO_NO_GAP` observado `GAP`
- `17:08` gap `-0.10` esperado `PLANO_NO_GAP` observado `GAP`
- `17:14` gap `-0.10` esperado `PLANO_NO_GAP` observado `GAP`
- `17:17` gap `0.20` esperado `PLANO_NO_GAP` observado `GAP`
- `17:19` gap `-0.10` esperado `PLANO_NO_GAP` observado `GAP`
- `17:23` gap `0.20` esperado `PLANO_NO_GAP` observado `GAP`
