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

### For Bel//Eng parallel corpus
We chose Russian, Ukrainian and Bulgarian as our transfer languages. To run preprocessing of data, run-

```
bash preprocess-ted-transfer-multilingual2.sh
```

You can then finetune the model and evaluate it both from English and to English.

```
bash traineval_flores_bel_trf_eng.sh
bash traineval_flores_eng_trf_bel.sh
```

## Improving Multilingual Translation using Data Augmentation
### Parallel data
We chose the Tatoeba challenge (https://opus.nlpl.eu/Tatoeba-v2021-07-22.php) and TED2020-v1 (https://opus.nlpl.eu/TED2020-v1.php) corpora as our additional parallel data.
The following does parallel data augmentation for AZE//ENG and BEL//ENG language pairs:

```bash
python augment_data.py parallel
```

You can then preprocess and finetune the model and evaluate it both from English and to English. Here `TatTed` is a unique augmentation tag to store parallel data and model checkpoints.

```bash
bash preprocess-ted-flores-bilingual-aug.sh TatTed
bash traineval_flores_aze_eng_aug.sh TatTed
bash traineval_flores_eng_aze_aug.sh TatTed

bash preprocess-ted-flores-bilingual2-aug.sh TatTed
bash traineval_flores_bel_eng_aug.sh TatTed
bash traineval_flores_eng_bel_aug.sh TatTed
```

### Back-translated data
We chose the QED corpus (https://opus.nlpl.eu/QED-v2.0a.php) as our source for monolingual data. 

The following downloads the monolingual AZE, BEL data and uses the above finetuned models to generate their English translations. Together, these back-translated monolingual-synthetic data are augmented to the existing parallel data.

```bash
python augment_data.py mono-aze-bel-synth-eng
```

You can then preprocess and finetune the above models and evaluate it for translations from English to Azerbaijani and Belorussian. Here `TatTedQed` is a unique augmentation tag to store parallel & back-translated data and model checkpoints, while `TatTed` is used to identify the corresponding best checkpoint to initialize our Eng->Aze/Bel models.

```bash
bash preprocess-ted-flores-bilingual-aug.sh TatTedQed
bash traineval_flores_eng_aze_aug.sh TatTedQed TatTed

bash preprocess-ted-flores-bilingual2-aug.sh TatTedQed
bash traineval_flores_eng_bel_aug.sh TatTedQed TatTed
```

Next, you can download the monolingual ENG data and use the above finetuned models to generate their Azerbaijani and Belorussian translations. Together, these back-translated monolingual-synthetic data are augmented to the existing parallel data.

```bash
python augment_data.py mono-eng-synth-aze-bel
```

You can then preprocess and finetune the above models and evaluate it for translations from Azerbaijani and Belorussian from English. Here `TatTedQed` is a unique augmentation tag to store parallel & back-translated data and model checkpoints, while `TatTed` is used to identify the corresponding best checkpoint to initialize our Aze/Bel->Eng models.

```bash
bash preprocess-ted-flores-bilingual-aug.sh TatTedQed
bash traineval_flores_aze_eng_aug.sh TatTedQed TatTed

bash preprocess-ted-flores-bilingual2-aug.sh TatTedQed
bash traineval_flores_bel_eng_aug.sh TatTedQed TatTed
```
