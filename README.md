# mnlp22-hw2-mt
Multilingual NLP '22 HW2 Machine Translation

## Data
To download the full data zip of Eng//Aze, Eng//Bel parallel data, please see this [link](https://drive.google.com/file/d/1kja_P-r-Z2bli67tz7pMChINzhRlLytX/view?usp=sharing)

## Improving Multilingual Transfer using transfer languages
### For Eng//Aze parallel corpus
We chose Turkish, Persian, Hungarian and Korean as our transfer languages. To run preprocessing of data, run-

```
bash preprocess-ted-transfer-multilingual.sh
```

You can then finetune the model and evaluate it both from English and to English.

```
bash traineval_flores_aze_trf_eng.sh
bash traineval_flores_eng_trf_aze.sh
```

### For Bel//Aze parallel corpus
We chose Russian, Ukrainian and Bulgarian as our transfer languages. To run preprocessing of data, run-

```
bash preprocess-ted-transfer-multilingual2.sh
```

You can then finetune the model and evaluate it both from English and to English.

```
bash traineval_flores_bel_trf_eng.sh
bash traineval_flores_eng_trf_bel.sh
```
