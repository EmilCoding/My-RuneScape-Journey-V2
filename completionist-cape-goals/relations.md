# Relations between the completionist achievments

```mermaid
---
title: Relations between the completionist achievments
---
graph TD
    QC[Quest Cape]
    MC[Max Cape]
    MQC[Master Quest Cape]
    MMC[Master Max Cape]
    CC[Completionist cape]
    TCC[Trimmed Completionist cape]
    MCC[Master Completionist cape]
    CTCC[Master Trimmed Completionist cape]

    QC --> MQC
    QC --> CC
    MC --> CC
    MC --> MMC
    CC --> TCC
    MQC --> TCC
    CC --> MCC
    MMC --> MCC
    TCC --> CTCC
    MCC --> CTCC
```

