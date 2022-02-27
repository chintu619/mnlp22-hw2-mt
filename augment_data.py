import os
import shutil
import argparse


def download_and_extract_parallel_corpus(url, lang='az'):
    if lang == 'az':
        os.makedirs(url[1]+url[2], exist_ok=True)
        os.popen(f"wget {url[0]} -O {url[1]+url[2]+'/az-en.txt.zip'}").read()
        os.popen(f"cd {url[1]+url[2]}; unzip -o az-en.txt.zip").read()
        eng_src = f"{url[1]+url[2]}/{url[2]}.az-en.en"
        aze_src = f"{url[1]+url[2]}/{url[2]}.az-en.az"
        eng_org = ["data/ted_raw/aze_eng/ted-train.orig.eng",
                   "data/ted_raw/aze_eng/ted-dev.orig.eng",
                   "data/ted_raw/aze_eng/ted-test.orig.eng"]
        raw_lines = set()
        for file in eng_org:
            with open(file) as f:
                raw_lines.update([line.rstrip().translate(str.maketrans('','','" ?;:!@-—$#&%.,\'')) for line in f.readlines()])
        raw_lines = "".join(raw_lines)
        with open(eng_src) as fe, open(aze_src) as fa:
            corpus_lines_eng = []
            corpus_lines_aze = []
            eng_lines = [line.rstrip() for line in fe.readlines()]
            aze_lines = [line.rstrip() for line in fa.readlines()]
            for ix,line in enumerate(eng_lines):
                line = line.replace("--","—")
                if line and (line.translate(str.maketrans('','','" ?;:!@-—$#&%.,\'')) not in raw_lines):
                    corpus_lines_eng.append(line)
                    corpus_lines_aze.append(aze_lines[ix])
        with open(url[1]+f"ted-train.{url[2]}.eng", 'w') as fe, \
             open(url[1]+f"ted-train.{url[2]}.aze", 'w') as fa:
            for line in corpus_lines_eng:
                fe.write(line+'\n')
            for line in corpus_lines_aze:
                fa.write(line+'\n')
    elif lang == 'be':
        os.makedirs(url[1]+url[2], exist_ok=True)
        os.popen(f"wget {url[0]} -O {url[1]+url[2]+'/be-en.txt.zip'}").read()
        os.popen(f"cd {url[1]+url[2]}; unzip -o be-en.txt.zip").read()
        eng_src = f"{url[1]+url[2]}/{url[2]}.be-en.en"
        bel_src = f"{url[1]+url[2]}/{url[2]}.be-en.be"
        eng_org = ["data/ted_raw/bel_eng/ted-train.orig.eng",
                   "data/ted_raw/bel_eng/ted-dev.orig.eng",
                   "data/ted_raw/bel_eng/ted-test.orig.eng"]
        raw_lines = set()
        for file in eng_org:
            with open(file) as f:
                raw_lines.update([line.rstrip().translate(str.maketrans('','','" ?;:!@-—$#&%.,\'')) for line in f.readlines()])
        raw_lines = "".join(raw_lines)
        with open(eng_src) as fe, open(bel_src) as fa:
            corpus_lines_eng = []
            corpus_lines_bel = []
            eng_lines = [line.rstrip() for line in fe.readlines()]
            bel_lines = [line.rstrip() for line in fa.readlines()]
            for ix,line in enumerate(eng_lines):
                line = line.replace("--","—")
                if line and (line.translate(str.maketrans('','','" ?;:!@-—$#&%.,\'')) not in raw_lines):
                    corpus_lines_eng.append(line)
                    corpus_lines_bel.append(bel_lines[ix])
        with open(url[1]+f"ted-train.{url[2]}.eng", 'w') as fe, \
             open(url[1]+f"ted-train.{url[2]}.bel", 'w') as fa:
            for line in corpus_lines_eng:
                fe.write(line+'\n')
            for line in corpus_lines_bel:
                fa.write(line+'\n')
    return


def download_and_extract_monolingual_corpus(url, lang='az'):
    if lang == 'az':
        os.makedirs(url[1]+url[2], exist_ok=True)
        os.popen(f"wget {url[0]} -O {url[1]+url[2]+'/az-en.txt.zip'}").read()
        os.popen(f"cd {url[1]+url[2]}; unzip -o az-en.txt.zip").read()
        eng_src = f"{url[1]+url[2]}/{url[2]}.az-en.en"
        aze_src = f"{url[1]+url[2]}/{url[2]}.az-en.az"
        eng_org = ["data/ted_raw/aze_eng/ted-train.orig.eng",
                   "data/ted_raw_aug/aze_eng/ted-train.TED2020.eng",
                   "data/ted_raw_aug/aze_eng/ted-train.Tatoeba.eng"]
        vocab = set()
        for file in eng_org:
            with open(file) as f:
                for line in f.readlines():
                    vocab.update(line.rstrip().translate(str.maketrans('','','"?;:!@-—$#&%.,\'')).lower().split())
        with open(eng_src) as fe, open(aze_src) as fa:
            corpus_lines_eng = []
            corpus_lines_aze = []
            eng_lines = [line.rstrip() for line in fe.readlines()]
            aze_lines = [line.rstrip() for line in fa.readlines()]
            for ix,line in enumerate(eng_lines):
                line = line.replace("--","—")
                if not line: continue
                line_words = set(line.translate(str.maketrans('','','"?;:!@-—$#&%.,\'')).lower().split())
                new_words = line_words.difference(vocab)
                if len(new_words) > 0.05*len(line_words): continue
                corpus_lines_eng.append(line)
                corpus_lines_aze.append(aze_lines[ix])
        with open(url[1]+f"ted-train.mono-{url[2]}.eng", 'w') as fe, \
             open(url[1]+f"ted-train.mono-{url[2]}.aze", 'w') as fa:
            for line in corpus_lines_eng:
                fe.write(line+'\n')
            for line in corpus_lines_aze:
                fa.write(line+'\n')
    elif lang == 'be':
        os.makedirs(url[1]+url[2], exist_ok=True)
        os.popen(f"wget {url[0]} -O {url[1]+url[2]+'/be-en.txt.zip'}").read()
        os.popen(f"cd {url[1]+url[2]}; unzip -o be-en.txt.zip").read()
        eng_src = f"{url[1]+url[2]}/{url[2]}.be-en.en"
        bel_src = f"{url[1]+url[2]}/{url[2]}.be-en.be"
        eng_org = ["data/ted_raw/bel_eng/ted-train.orig.eng",
                   "data/ted_raw_aug/bel_eng/ted-train.TED2020.eng",
                   "data/ted_raw_aug/bel_eng/ted-train.Tatoeba.eng"]
        vocab = set()
        for file in eng_org:
            with open(file) as f:
                for line in f.readlines():
                    vocab.update(line.rstrip().translate(str.maketrans('','','"?;:!@-—$#&%.,\'')).lower().split())
        with open(eng_src) as fe, open(bel_src) as fa:
            corpus_lines_eng = []
            corpus_lines_bel = []
            eng_lines = [line.rstrip() for line in fe.readlines()]
            bel_lines = [line.rstrip() for line in fa.readlines()]
            for ix,line in enumerate(eng_lines):
                line = line.replace("--","—")
                if not line: continue
                line_words = set(line.translate(str.maketrans('','','"?;:!@-—$#&%.,\'')).lower().split())
                new_words = line_words.difference(vocab)
                if len(new_words) > 0.05*len(line_words): continue
                corpus_lines_eng.append(line)
                corpus_lines_bel.append(bel_lines[ix])
        with open(url[1]+f"ted-train.mono-{url[2]}.eng", 'w') as fe, \
             open(url[1]+f"ted-train.mono-{url[2]}.bel", 'w') as fa:
            for line in corpus_lines_eng:
                fe.write(line+'\n')
            for line in corpus_lines_bel:
                fa.write(line+'\n')
    return

if __name__ == "__main__":
    # Create the parser and add arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('augmentation', default='parallel', type=str, 
                        choices=['parallel', 'mono-aze-bel-synth-eng', 'mono-eng-synth-aze-bel'])

    # Parse and print the results
    args = parser.parse_args()

    if args.augmentation == 'parallel':
        # ---------------- parallel-AZE-ENG ----------------
        url_ted2020_az_en = ("https://object.pouta.csc.fi/OPUS-TED2020/v1/moses/az-en.txt.zip", 
                             'data/ted_raw_aug/aze_eng/', 'TED2020')
        url_tatoeba_az_en = ("https://object.pouta.csc.fi/OPUS-Tatoeba/v2021-07-22/moses/az-en.txt.zip", 
                             'data/ted_raw_aug/aze_eng/', 'Tatoeba')
        for url in [url_ted2020_az_en, url_tatoeba_az_en]: 
            download_and_extract_parallel_corpus(url, lang='az')

        shutil.copyfile("data/ted_raw/aze_eng/ted-train.orig.aze", "data/ted_raw_aug/aze_eng/ted-train.orig.aze")
        shutil.copyfile("data/ted_raw/aze_eng/ted-train.orig.eng", "data/ted_raw_aug/aze_eng/ted-train.orig.eng")
        augmentations = ['Tatoeba', 'TED2020']
        for aug in augmentations:
            os.popen(f"cat data/ted_raw_aug/aze_eng/ted-train.{aug}.aze >> data/ted_raw_aug/aze_eng/ted-train.orig.aze").read()
            os.popen(f"cat data/ted_raw_aug/aze_eng/ted-train.{aug}.eng >> data/ted_raw_aug/aze_eng/ted-train.orig.eng").read()

        # ---------------- parallel-BEL-ENG ----------------
        url_ted2020_be_en = ("https://object.pouta.csc.fi/OPUS-TED2020/v1/moses/be-en.txt.zip", 
                             'data/ted_raw_aug/bel_eng/', 'TED2020')
        url_tatoeba_be_en = ("https://object.pouta.csc.fi/OPUS-Tatoeba/v2021-07-22/moses/be-en.txt.zip", 
                             'data/ted_raw_aug/bel_eng/', 'Tatoeba')
        for url in [url_ted2020_be_en, url_tatoeba_be_en]: 
            download_and_extract_parallel_corpus(url, lang='be')

        shutil.copyfile("data/ted_raw/bel_eng/ted-train.orig.bel", "data/ted_raw_aug/bel_eng/ted-train.orig.bel")
        shutil.copyfile("data/ted_raw/bel_eng/ted-train.orig.eng", "data/ted_raw_aug/bel_eng/ted-train.orig.eng")
        augmentations = ['Tatoeba', 'TED2020']
        for aug in augmentations:
            os.popen(f"cat data/ted_raw_aug/bel_eng/ted-train.{aug}.bel >> data/ted_raw_aug/bel_eng/ted-train.orig.bel").read()
            os.popen(f"cat data/ted_raw_aug/bel_eng/ted-train.{aug}.eng >> data/ted_raw_aug/bel_eng/ted-train.orig.eng").read()


    elif args.augmentation == 'mono-aze-bel-synth-eng':
        # ---------------- monolingual-AZE+synthetic-ENG  ----------------
        url_qed_az = ("https://object.pouta.csc.fi/OPUS-QED/v2.0a/moses/az-en.txt.zip", 
                      'data/ted_raw_aug/aze_eng/', 'QED')
        # download QED corpus for monolingual AZE data
        for url in [url_qed_az]:
            download_and_extract_monolingual_corpus(url, lang='az')
        # back-translate AZE to ENG using pretrained model
        os.popen("bash backtranslate_flores_aze_eng_aug.sh TatTedQed TatTed").read()
        # copy the original training data
        shutil.copyfile("data/ted_raw/aze_eng/ted-train.orig.aze", "data/ted_raw_aug/aze_eng/ted-train.orig.aze")
        shutil.copyfile("data/ted_raw/aze_eng/ted-train.orig.eng", "data/ted_raw_aug/aze_eng/ted-train.orig.eng")
        # possible augmentations for AZE and ENG respectively in each tuple
        augmentations = [('Tatoeba','Tatoeba'), 
                         ('TED2020','TED2020'), 
                         ('mono-QED','synth-QED')]
        for aug in augmentations:
            os.popen(f"cat data/ted_raw_aug/aze_eng/ted-train.{aug[0]}.aze >> data/ted_raw_aug/aze_eng/ted-train.orig.aze").read()
            os.popen(f"cat data/ted_raw_aug/aze_eng/ted-train.{aug[1]}.eng >> data/ted_raw_aug/aze_eng/ted-train.orig.eng").read()

        # ---------------- monolingual-BEL+synthetic-ENG  ----------------
        url_qed_be = ("https://object.pouta.csc.fi/OPUS-QED/v2.0a/moses/be-en.txt.zip", 
                      'data/ted_raw_aug/bel_eng/', 'QED')
        # download QED corpus for monolingual BEL data
        for url in [url_qed_be]:
            download_and_extract_monolingual_corpus(url, lang='be')
        # back-translate BEL to ENG using pretrained model
        os.popen("bash backtranslate_flores_bel_eng_aug.sh TatTedQed TatTed").read()
        # copy the original training data
        shutil.copyfile("data/ted_raw/bel_eng/ted-train.orig.bel", "data/ted_raw_aug/bel_eng/ted-train.orig.bel")
        shutil.copyfile("data/ted_raw/bel_eng/ted-train.orig.eng", "data/ted_raw_aug/bel_eng/ted-train.orig.eng")
        # possible augmentations for BEL and ENG respectively in each tuple
        augmentations = [('Tatoeba','Tatoeba'), 
                         ('TED2020','TED2020'), 
                         ('mono-QED','synth-QED')]
        for aug in augmentations:
            os.popen(f"cat data/ted_raw_aug/bel_eng/ted-train.{aug[0]}.bel >> data/ted_raw_aug/bel_eng/ted-train.orig.bel").read()
            os.popen(f"cat data/ted_raw_aug/bel_eng/ted-train.{aug[1]}.eng >> data/ted_raw_aug/bel_eng/ted-train.orig.eng").read()


    elif args.augmentation == 'mono-eng-synth-aze-bel':
        # ---------------- monolingual-ENG+synthetic-AZE ----------------
        # back-translate ENG to AZE using pretrained model
        os.popen("bash backtranslate_flores_eng_aze_aug.sh TatTedQed TatTedQed").read()
        # copy the original training data
        shutil.copyfile("data/ted_raw/aze_eng/ted-train.orig.aze", "data/ted_raw_aug/aze_eng/ted-train.orig.aze")
        shutil.copyfile("data/ted_raw/aze_eng/ted-train.orig.eng", "data/ted_raw_aug/aze_eng/ted-train.orig.eng")
        # possible augmentations for AZE and ENG respectively in each tuple
        augmentations = [('Tatoeba','Tatoeba'), 
                         ('TED2020','TED2020'), 
                         ('synth-QED','mono-QED')]
        for aug in augmentations:
            os.popen(f"cat data/ted_raw_aug/aze_eng/ted-train.{aug[0]}.aze >> data/ted_raw_aug/aze_eng/ted-train.orig.aze").read()
            os.popen(f"cat data/ted_raw_aug/aze_eng/ted-train.{aug[1]}.eng >> data/ted_raw_aug/aze_eng/ted-train.orig.eng").read()

        # ---------------- monolingual-ENG+synthetic-BEL ----------------
        # back-translate ENG to BEL using pretrained model
        os.popen("bash backtranslate_flores_eng_bel_aug.sh TatTedQed TatTedQed").read()
        # copy the original training data
        shutil.copyfile("data/ted_raw/bel_eng/ted-train.orig.bel", "data/ted_raw_aug/bel_eng/ted-train.orig.bel")
        shutil.copyfile("data/ted_raw/bel_eng/ted-train.orig.eng", "data/ted_raw_aug/bel_eng/ted-train.orig.eng")
        # possible augmentations for BEL and ENG respectively in each tuple
        augmentations = [('Tatoeba','Tatoeba'), 
                         ('TED2020','TED2020'), 
                         ('synth-QED','mono-QED')]
        for aug in augmentations:
            os.popen(f"cat data/ted_raw_aug/bel_eng/ted-train.{aug[0]}.bel >> data/ted_raw_aug/bel_eng/ted-train.orig.bel").read()
            os.popen(f"cat data/ted_raw_aug/bel_eng/ted-train.{aug[1]}.eng >> data/ted_raw_aug/bel_eng/ted-train.orig.eng").read()
