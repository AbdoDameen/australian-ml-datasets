# 20 DATASET CATALOG — Daily ML Datasets

Curated high-quality datasets across biology, ecology, medicine, environmental science, genomics, neuroscience, and more. Each entry has source, format, size, and ML potential.

---

## HOW TO USE

Each day, pick one dataset from this catalog. I'll:
1. Download/ingest the data
2. Run the full SEIFA-style pipeline (clean → feature engineer → ML-ready)
3. Save to `datasets/[domain]/[dataset-name]/`
4. Document with README, metadata, and process doc
5. Commit and push to GitHub

---

## DATASET 1: Heart Disease (Cleveland/UCI)
**Domain:** Medicine, Cardiology
**Source:** UCI ML Repository — https://archive.ics.uci.edu/ml/datasets/heart+disease
**Format:** CSV (processed.cleveland.data)
**Rows:** 303 patients, 76 attributes (commonly 14 used)
**Target:** Presence of heart disease (0-4)
**ML Tasks:** Classification, risk prediction
**Citation:** Detrano, R., et al. (1989). International application of a new probability algorithm for the diagnosis of coronary artery disease.
**Download:** https://archive.ics.uci.edu/static/public/45/heart+disease.zip

---

## DATASET 2: Gene Expression Cancer (RNA-Seq)
**Domain:** Cancer, Genomics, Molecular Biology
**Source:** UCI ML Repository — https://archive.ics.uci.edu/dataset/401/gene+expression+cancer+rna+seq
**Format:** CSV
**Rows:** 801 patients, 20,531 genes
**Target:** Cancer type (5 types: BRCA, KIRC, COAD, LUAD, PRAD)
**ML Tasks:** Multi-class classification, feature selection (dimension reduction)
**Citation:** Weinstein, J. N., et al. (2013). The Cancer Genome Atlas Pan-Cancer analysis project.
**Download:** https://archive.ics.uci.edu/static/public/401/gene+expression+cancer+rna+seq.zip

---

## DATASET 3: Climate Change Sentiment & Earth Surface Temperature
**Domain:** Climate Science, Environmental Science
**Source:** Berkeley Earth / Kaggle — https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data
**Format:** CSV
**Rows:** 8,592,000+ (global temperature records)
**Target:** Land Average Temperature
**ML Tasks:** Time series forecasting, anomaly detection, trend analysis
**Citation:** Berkeley Earth. "Climate Change: Earth Surface Temperature Data."
**Download:** https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data

---

## DATASET 4: Wine Quality
**Domain:** Chemistry, Food Science
**Source:** UCI ML Repository — https://archive.ics.uci.edu/ml/datasets/wine+quality
**Format:** CSV (two files: red + white)
**Rows:** 4,898 (red: 1,599, white: 4,898)
**Target:** Wine quality score (0-10)
**ML Tasks:** Regression, classification, feature importance
**Citation:** Cortez, P., et al. (2009). Modeling wine preferences by data mining from physicochemical properties.
**Download:** https://archive.ics.uci.edu/static/public/186/wine+quality.zip

---

## DATASET 5: Mushroom Classification
**Domain:** Mycology, Biology
**Source:** UCI ML Repository — https://archive.ics.uci.edu/ml/datasets/mushroom
**Format:** CSV
**Rows:** 8,124 mushroom samples
**Target:** Edible vs Poisonous
**ML Tasks:** Binary classification, categorical feature encoding
**Citation:** Schlimmer, J. (1987). Mushroom records drawn from The Audubon Society Field Guide to North American Mushrooms.
**Download:** https://archive.ics.uci.edu/static/public/73/mushroom.zip

---

## DATASET 6: Epileptic Seizure Recognition
**Domain:** Neuroscience, Neurology, Mental Health
**Source:** UCI ML Repository — https://archive.ics.uci.edu/ml/datasets/Epileptic+Seizure+Recognition
**Format:** CSV
**Rows:** 11,500 EEG readings across 500 patients
**Target:** Seizure vs non-seizure (5 classes)
**ML Tasks:** Time series classification, signal processing
**Citation:** Andrzejak, R. G., et al. (2001). Indications of nonlinear deterministic and finite-dimensional structures in time series of brain electrical activity.
**Download:** https://archive.ics.uci.edu/static/public/388/epileptic+seizure+recognition.zip

---

## DATASET 7: Dengue Cases Prediction
**Domain:** Infectious Diseases, Epidemiology, Public Health
**Source:** DrivenData — https://www.drivendata.org/competitions/44/dengai-predicting-disease-spread/
**Format:** CSV
**Rows:** 1,456 (weekly data from San Juan, Iquitos)
**Target:** Total dengue cases per week
**ML Tasks:** Time series regression, environmental covariates
**Citation:** DrivenData. "DengAI: Predicting Disease Spread."
**Download:** https://www.drivendata.org/competitions/44/dengai-predicting-disease-spread/data/

---

## DATASET 8: Breast Cancer Wisconsin (Diagnostic)
**Domain:** Cancer, Medicine
**Source:** UCI ML Repository — https://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Wisconsin+(Diagnostic)
**Format:** CSV
**Rows:** 569 patients, 30 features
**Target:** Malignant vs Benign
**ML Tasks:** Binary classification
**Citation:** Wolberg, W. H., et al. (1995). Breast cancer diagnosis and prognosis via quantitative image analysis.
**Download:** https://archive.ics.uci.edu/static/public/17/breast+cancer+wisconsin+diagnostic.zip

---

## DATASET 9: Protein Localization Sites (E. coli)
**Domain:** Cell Biology, Microbiology, Molecular Biology
**Source:** UCI ML Repository — https://archive.ics.uci.edu/ml/datasets/Ecoli
**Format:** CSV
**Rows:** 336 E. coli proteins, 8 features
**Target:** Localization site (8 classes)
**ML Tasks:** Multi-class classification
**Citation:** Horton, P., & Nakai, K. (1996). A probabilistic classification system for predicting the cellular localization sites of proteins.
**Download:** https://archive.ics.uci.edu/static/public/39/ecoli.zip

---

## DATASET 10: Optical Recognition of Handwritten Digits
**Domain:** Computer Vision, Pattern Recognition
**Source:** UCI ML Repository — https://archive.ics.uci.edu/ml/datasets/Optical+Recognition+of+Handwritten+Digits
**Format:** CSV
**Rows:** 5,620 digits (training) + 1,780 (test), 64 features
**Target:** Digit (0-9)
**ML Tasks:** Multi-class classification, image processing
**Citation:** Alpaydin, E., & Kaynak, C. (1998). Cascading classifiers for handwritten digit recognition.
**Download:** https://archive.ics.uci.edu/static/public/80/optical+recognition+of+handwritten+digits.zip

---

## DATASET 11: Adult Census Income
**Domain:** Sociology, Economics, Public Policy
**Source:** UCI ML Repository — https://archive.ics.uci.edu/ml/datasets/adult
**Format:** CSV
**Rows:** 48,842 individuals, 14 attributes
**Target:** Income >50K vs <=50K
**ML Tasks:** Binary classification, fairness analysis
**Citation:** Kohavi, R. (1996). Scaling up the accuracy of naive-Bayes classifiers: a decision-tree hybrid.
**Download:** https://archive.ics.uci.edu/static/public/2/adult.zip

---

## DATASET 12: Drug Review Dataset (Drugs.com)
**Domain:** Pharmacology, Medicine, Drug Development
**Source:** UCI ML Repository — https://archive.ics.uci.edu/ml/datasets/Drug+Review+Dataset+(Drugs.com)
**Format:** TSV
**Rows:** 215,063 drug reviews
**Target:** Drug rating (1-10), condition, sentiment
**ML Tasks:** Sentiment analysis, NLP, recommendation
**Citation:** Gräßer, F., et al. (2018). A dataset for drug review analysis.
**Download:** https://archive.ics.uci.edu/static/public/462/drug+review+dataset+drugs+com.zip

---

## DATASET 13: Human Activity Recognition (Smartphone)
**Domain:** Biophysics, Health Informatics
**Source:** UCI ML Repository — https://archive.ics.uci.edu/ml/datasets/Human+Activity+Recognition+Using+Smartphones
**Format:** CSV / TXT
**Rows:** 10,299 samples, 561 features
**Target:** Activity (6 types: walking, sitting, standing, etc.)
**ML Tasks:** Multi-class classification, time series
**Citation:** Anguita, D., et al. (2013). A public domain dataset for human activity recognition using smartphones.
**Download:** https://archive.ics.uci.edu/static/public/240/human+activity+recognition+using+smartphones.zip

---

## DATASET 14: Forest Cover Type
**Domain:** Ecology, Environmental Science, Geography
**Source:** UCI ML Repository — https://archive.ics.uci.edu/ml/datasets/covertype
**Format:** CSV
**Rows:** 581,012 forest cells, 54 features
**Target:** Forest cover type (7 classes)
**ML Tasks:** Multi-class classification, geospatial, large-scale
**Citation:** Blackard, J. A., & Dean, D. J. (1999). Comparative accuracies of artificial neural networks and discriminant analysis in predicting forest cover types from cartographic variables.
**Download:** https://archive.ics.uci.edu/static/public/31/covertype.zip

---

## DATASET 15: Physicochemical Properties of Protein Tertiary Structure
**Domain:** Biochemistry, Molecular Biology, Biophysics
**Source:** UCI ML Repository — https://archive.ics.uci.edu/ml/datasets/Physicochemical+Properties+of+Protein+Tertiary+Structure
**Format:** CSV
**Rows:** 45,730 protein samples, 9 features
**Target:** RMSD (protein folding size)
**ML Tasks:** Regression
**Citation:** Rana, P. (2013). Physicochemical properties of protein tertiary structure data set.
**Download:** https://archive.ics.uci.edu/static/public/265/physicochemical+properties+of+protein+tertiary+structure.zip

---

## DATASET 16: Twitter Cyberbullying Detection
**Domain:** Psychology, Mental Health, NLP
**Source:** Kaggle — https://www.kaggle.com/datasets/andrewmvd/cyberbullying-classification
**Format:** CSV
**Rows:** 47,000+ tweets
**Target:** Cyberbullying type (6 categories: race, gender, religion, etc.)
**ML Tasks:** NLP multi-class classification, text preprocessing
**Citation:** Cyberbullying Classification dataset. Kaggle.
**Download:** https://www.kaggle.com/datasets/andrewmvd/cyberbullying-classification

---

## DATASET 17: Diabetic Retinopathy Detection
**Domain:** Medicine, Ophthalmology, Computer Vision
**Source:** Kaggle — https://www.kaggle.com/c/diabetic-retinopathy-detection
**Format:** Images + CSV labels
**Rows:** 35,126 retina images (training)
**Target:** Retinopathy severity (0-4)
**ML Tasks:** Image classification, medical imaging
**Citation:** Kaggle. "Diabetic Retinopathy Detection." 2015.
**Download:** https://www.kaggle.com/c/diabetic-retinopathy-detection/data

---

## DATASET 18: Australian Tourism Data (Visitor Numbers)
**Domain:** Sociology, Economics, Geography (Australian-specific)
**Source:** Tourism Australia / data.gov.au — https://data.gov.au/dataset/ds-dga-abc1a6c3-7b79-4e99-ae34-1f52cbeadc3f
**Format:** CSV
**Rows:** 10,000+ rows (monthly visitor data by region/country of origin)
**Target:** Visitor arrivals
**ML Tasks:** Time series forecasting, regression
**Citation:** Tourism Research Australia. "International Visitor Survey."
**Download:** https://data.gov.au/dataset/ds-dga-abc1a6c3-7b79-4e99-ae34-1f52cbeadc3f

---

## DATASET 19: Ocean Water Quality (NSW Beachwatch)
**Domain:** Oceanography, Marine Biology, Environmental Science
**Source:** NSW Government / data.nsw.gov.au — https://data.nsw.gov.au/data/dataset/beachwatch-water-quality
**Format:** CSV
**Rows:** 50,000+ water quality samples across NSW beaches
**Target:** Water quality grade (A-D) / Enterococci levels
**ML Tasks:** Classification, regression, environmental monitoring
**Citation:** NSW Department of Planning and Environment. "Beachwatch Water Quality."
**Download:** https://data.nsw.gov.au/data/dataset/beachwatch-water-quality

---

## DATASET 20: Genomic Data — DARPA DNA Sequencing (Synthetic)
**Domain:** Genomics, Computational Biology
**Source:** Kaggle — https://www.kaggle.com/datasets/nicklaus/gene-sequences-dataset
**Format:** CSV / FASTA
**Rows:** 10,000+ gene sequences with attributes
**Target:** Gene family classification
**ML Tasks:** Sequence classification, bioinformatics
**Citation:** Gene Sequences Dataset. Kaggle.
**Download:** https://www.kaggle.com/datasets/nicklaus/gene-sequences-dataset

---

## DATASET 21: Air Quality (Beijing PM2.5)
**Domain:** Environmental Engineering, Environmental Technologies, Climate Science
**Source:** UCI ML Repository — https://archive.ics.uci.edu/ml/datasets/Beijing+PM2.5+Data
**Format:** CSV
**Rows:** 43,824 hourly readings (2010-2014)
**Target:** PM2.5 concentration
**ML Tasks:** Regression, time series forecasting
**Citation:** Liang, X., et al. (2015). Assessing Beijing's PM2.5 pollution.
**Download:** https://archive.ics.uci.edu/static/public/381/beijing+pm2+5+data.zip

---

## DATASET 22: DNA Methylation (Breast Cancer)
**Domain:** Epigenetics, Cancer, Genomics
**Source:** NCBI GEO / ArrayExpress — https://www.ebi.ac.uk/biostudies/arrayexpress/studies/E-GEOD-51032
**Format:** CSV
**Rows:** 485,000 CpG sites, 96 samples
**Target:** Cancer vs normal
**ML Tasks:** Binary classification, high-dimensional feature selection
**Citation:** E-GEOD-51032. DNA methylation profiling in breast cancer.
**Download:** https://www.ebi.ac.uk/biostudies/arrayexpress/studies/E-GEOD-51032

---

## DATASET 23: EEG Brainwave (Alcoholism)
**Domain:** Neurology, Neuroscience, Neurogenetics
**Source:** UCI ML Repository — https://archive.ics.uci.edu/ml/datasets/EEG+Database
**Format:** CSV
**Rows:** 14,980 recordings, 122 subjects
**Target:** Alcoholic vs Control
**ML Tasks:** Classification, signal processing
**Citation:** Zhang, X. L., et al. (1995). EEG database.
**Download:** https://archive.ics.uci.edu/static/public/121/eeg+database.zip

---

## DATASET 24: Food Nutrition (USDA)
**Domain:** Food Chemistry, Food Nutritional Balance
**Source:** USDA FoodData Central — https://fdc.nal.usda.gov/
**Format:** CSV / JSON
**Rows:** 7,800+ foods, 80+ nutrients
**Target:** Food category / nutrient content
**ML Tasks:** Classification, regression, clustering
**Citation:** USDA ARS. FoodData Central, 2019.
**Download:** https://fdc.nal.usda.gov/download-datasets.html

---

## DATASET 25: Chest X-Ray (Pneumonia)
**Domain:** Radiology, Medical Imaging, Paediatrics
**Source:** Kaggle — https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia
**Format:** Images (JPEG) + CSV labels
**Rows:** 5,863 X-ray images
**Target:** Pneumonia detection
**ML Tasks:** Image classification, deep learning
**Citation:** Kermany, D. S., et al. (2018). Identifying medical diagnoses by image-based deep learning.
**Download:** https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia

---

## DATASET 26: Diabetes Readmission (Hospital)
**Domain:** Geriatrics, Public Health, Healthcare Admin
**Source:** UCI ML Repository — https://archive.ics.uci.edu/ml/datasets/Diabetes+130-US+hospitals+for+years+1999-2008
**Format:** CSV
**Rows:** 101,766 readmission records, 130 hospitals
**Target:** Readmitted within 30 days
**ML Tasks:** Binary classification, risk prediction
**Citation:** Strack, B., et al. (2014). Impact of HbA1c on hospital readmission rates.
**Download:** https://archive.ics.uci.edu/static/public/296/diabetes+130+us+hospitals+for+years+1999+2008.zip

---

## DATASET 27: Species Distribution (GBIF Australia)
**Domain:** Climate Change Impact, Ecology, Evolutionary Biology
**Source:** GBIF — https://www.gbif.org/
**Format:** CSV / Darwin Core
**Rows:** 1,000,000+ occurrence records
**Target:** Species presence/absence
**ML Tasks:** Binary classification, spatial modelling
**Citation:** GBIF.org. Free and open access to biodiversity data.
**Download:** https://www.gbif.org/occurrence/download?taxon_key=1

---

## DATASET 28: Liver Disease (Indian Liver Patient)
**Domain:** Gastroenterology, Hepatology
**Source:** UCI ML Repository — https://archive.ics.uci.edu/ml/datasets/ILPD+(Indian+Liver+Patient+Dataset)
**Format:** CSV
**Rows:** 583 patients, 10 attributes
**Target:** Liver disease presence
**ML Tasks:** Binary classification, diagnostic prediction
**Citation:** Ramana, B. V., et al. (2012). Liver patients from USA and India.
**Download:** https://archive.ics.uci.edu/static/public/225/ilpd+indian+liver+patient+dataset.zip

---

## DATASET 29: Crop Yields (Global)
**Domain:** GMOs, Food Science, Environmental Engineering
**Source:** Our World in Data — https://ourworldindata.org/crop-yields
**Format:** CSV
**Rows:** 80,000+ (1961-2022, 100+ crops, 200+ countries)
**Target:** Crop yield per hectare
**ML Tasks:** Time series, regression, causal inference
**Citation:** Our World in Data. Crop yields.
**Download:** https://github.com/owid/owid-datasets/raw/master/datasets/Crop%20yields/Crop%20yields.csv

---

## DATASET 30: Gene Therapy — Vector Engineering
**Domain:** Gene Therapy, Molecular Biology
**Source:** NCBI / AddGene — https://www.addgene.org/
**Format:** CSV (curated plasmid/viral vector dataset)
**Rows:** 5,000+ engineered genetic constructs
**Target:** Expression level / delivery efficiency
**ML Tasks:** Regression, sequence-based prediction
**Citation:** AddGene. Non-profit plasmid repository.
**Download:** https://www.addgene.org/browse/

---

## DATASET 31: Forest Fires (Portugal)
**Domain:** Forestry Fire Management, Environmental Science, Landscape Ecology
**Source:** UCI ML Repository — https://archive.ics.uci.edu/ml/datasets/Forest+Fires
**Format:** CSV
**Rows:** 517 forest fire records, 13 attributes
**Target:** Burned area (hectares)
**ML Tasks:** Regression, environmental modelling
**Citation:** Cortez, P., & Morais, A. (2007). A data mining approach to predict forest fires using meteorological data.
**Download:** https://archive.ics.uci.edu/static/public/162/forest+fires.zip

---

## DATASET 32: Chronic Kidney Disease
**Domain:** Nephrology, Urology, Medicine
**Source:** UCI ML Repository — https://archive.ics.uci.edu/ml/datasets/Chronic_Kidney_Disease
**Format:** CSV
**Rows:** 400 patient records, 25 attributes
**Target:** CKD vs Non-CKD
**ML Tasks:** Binary classification, medical diagnosis
**Citation:** Soundarapandian, P., et al. (2015). Chronic Kidney Disease dataset.
**Download:** https://archive.ics.uci.edu/static/public/336/chronic+kidney+disease.zip

---

## DATASET 33: Dermatology Dataset
**Domain:** Dermatology, Medicine
**Source:** UCI ML Repository — https://archive.ics.uci.edu/ml/datasets/Dermatology
**Format:** CSV
**Rows:** 366 patients, 34 attributes
**Target:** Erythematous diseases (6 classes: psoriasis, eczema, etc.)
**ML Tasks:** Multi-class classification
**Citation:** Nilsel Ilter, N., & Guler, N. (1998). Dermatology dataset.
**Download:** https://archive.ics.uci.edu/static/public/33/dermatology.zip

---

## DATASET 34: Gynecological Cancer (Endometrial/Uterine)
**Domain:** Oncology, Reproduction, Cancer Biology
**Source:** UCI ML Repository — https://archive.ics.uci.edu/ml/datasets/Uterine+Cancer+Radiogenomics
**Format:** CSV
**Rows:** 350+ patients, 1,000+ radiomic features
**Target:** Cancer subtype / prognosis
**ML Tasks:** Classification, feature selection, survival analysis
**Citation:** Radiogenomics of Uterine Cancer. UCI.
**Download:** https://archive.ics.uci.edu/static/public/627/uterine+cancer+radiogenomics.zip

---

## DATASET 35: Water Quality (River pH & Contaminants)
**Domain:** Freshwater Ecology, Hydrology, Environmental Engineering
**Source:** Kaggle — https://www.kaggle.com/datasets/adityakadiwal/water-potability
**Format:** CSV
**Rows:** 3,276 water samples, 10 quality metrics
**Target:** Water potability (Safe vs Unsafe)
**ML Tasks:** Binary classification, environmental monitoring
**Citation:** Kadiwal, A. Water Potability dataset. Kaggle.
**Download:** https://www.kaggle.com/datasets/adityakadiwal/water-potability

---

## DATASET 36: Clinical Sports Nutrition — Athlete Performance
**Domain:** Clinical Sports Nutrition, Nutritional Physiology
**Source:** Kaggle — https://www.kaggle.com/datasets/arashnic/fitbit-dataset
**Format:** CSV
**Rows:** 33,000+ daily Fitbit records, 30+ metrics
**Target:** Activity intensity / calorie expenditure
**ML Tasks:** Regression, time series, clustering
**Citation:** Fitbit Dataset. Kaggle.
**Download:** https://www.kaggle.com/datasets/arashnic/fitbit-dataset

---

## DATASET 37: Emergency Medicine — Triage & Outcomes
**Domain:** Emergency Medicine, Intensive Care, Health Care
**Source:** MIMIC-III / PhysioNet — https://physionet.org/content/mimiciii/1.4/
**Format:** CSV (relational database)
**Rows:** 53,423 ICU admissions, 50+ clinical features
**Target:** Mortality / ICU length of stay
**ML Tasks:** Classification, regression, survival analysis
**Citation:** Johnson, A., et al. (2016). MIMIC-III, a freely accessible critical care database.
**Download:** https://physionet.org/content/mimiciii/1.4/

---

## DATASET 38: Thyroid Disease (Endocrinology)
**Domain:** Endocrinology, Medical Genetics
**Source:** UCI ML Repository — https://archive.ics.uci.edu/ml/datasets/Thyroid+Disease
**Format:** CSV
**Rows:** 7,200+ patient records, 30 attributes
**Target:** Hyperthyroid vs Normal
**ML Tasks:** Binary classification, diagnostic prediction
**Citation:** Coiera, E. (1997). Thyroid Disease datasets.
**Download:** https://archive.ics.uci.edu/static/public/102/thyroid+disease.zip

---

## DATASET 39: Food Safety — Microbial Contamination
**Domain:** Food Packaging, Preservation and Safety, Food Engineering
**Source:** Kaggle — https://www.kaggle.com/datasets/cdc/foodborne-diseases
**Format:** CSV
**Rows:** 50,000+ foodborne illness outbreak records
**Target:** Pathogen type / severity
**ML Tasks:** Multi-class classification, outbreak pattern analysis
**Citation:** CDC Foodborne Disease Outbreak Surveillance System.
**Download:** https://www.kaggle.com/datasets/cdc/foodborne-diseases

---

## DATASET 40: Climatology — Australian Rainfall Patterns
**Domain:** Climatology, Climate Change Processes, Surface Water Hydrology
**Source:** Bureau of Meteorology / data.gov.au — http://www.bom.gov.au/climate/data/
**Format:** CSV
**Rows:** 100,000+ monthly rainfall records (100+ years, 1,000+ stations)
**Target:** Rainfall amount / drought classification
**ML Tasks:** Time series forecasting, regression, anomaly detection
**Citation:** Australian Bureau of Meteorology. Climate Data Online.
**Download:** http://www.bom.gov.au/climate/data/

---

## DATASET 41: Wine Chemistry & Quality (Portuguese Vinho Verde)
**Domain:** Oenology, Viticulture, Food Chemistry
**Source:** UCI ML Repository — https://archive.ics.uci.edu/ml/datasets/wine+quality
**Format:** CSV
**Rows:** 4,898 (red 1,599 + white 4,898)
**Target:** Wine quality score (0-10)
**ML Tasks:** Regression, classification, feature importance
**Citation:** Cortez, P., et al. (2009). Modeling wine preferences by data mining from physicochemical properties.
**Download:** https://archive.ics.uci.edu/static/public/186/wine+quality.zip

---

## DATASET 42: Cervical Cancer Risk Factors
**Domain:** Cancer Risk Factors, Oncology, Public Health
**Source:** UCI ML Repository — https://archive.ics.uci.edu/ml/datasets/Cervical+Cancer+(Risk+Factors)
**Format:** CSV
**Rows:** 858 patient records, 36 risk factors
**Target:** Cancer diagnosis (4 targets: Hinselmann, Schiller, Cytology, Biopsy)
**ML Tasks:** Classification, risk prediction
**Citation:** Fernandes, K., et al. (2017). Cervical cancer risk factors dataset.
**Download:** https://archive.ics.uci.edu/static/public/383/cervical+cancer+risk+factors.zip

---

## DATASET 43: Wildlife Tracking — Kangaroo Movement
**Domain:** Wildlife Management, Vertebrate Biology, Biogeography
**Source:** data.gov.au / Atlas of Living Australia — https://www.ala.org.au/
**Format:** CSV
**Rows:** 50,000+ species occurrence records (Australian macropods)
**Target:** Species presence / habitat suitability
**ML Tasks:** Classification, spatial modelling, species distribution
**Citation:** Atlas of Living Australia. Occurrence records.
**Download:** https://biocache.ala.org.au/occurrences/search?q=Macropus

---

## DATASET 44: Student Performance (Education)
**Domain:** Education, Educational Psychology, Social Psychology
**Source:** UCI ML Repository — https://archive.ics.uci.edu/ml/datasets/Student+Performance
**Format:** CSV
**Rows:** 1,044 students (649 math, 395 Portuguese), 30+ attributes
**Target:** Final grade (G3)
**ML Tasks:** Regression, classification, educational data mining
**Citation:** Cortez, P., & Silva, A. (2008). Using data mining to predict secondary school student performance.
**Download:** https://archive.ics.uci.edu/static/public/320/student+performance.zip

---

## DATASET 45: Carbon Flux Prediction (FLUXNET)
**Domain:** Carbon Sequestration Science, Climate Change Processes
**Source:** FLUXNET / OzFlux (Australian) — https://www.ozflux.org.au/
**Format:** CSV
**Rows:** 500,000+ hourly CO2 flux measurements from Australian towers
**Target:** Net ecosystem exchange (NEE) of CO2
**ML Tasks:** Time series regression, environmental modelling
**Citation:** OzFlux. Australian and New Zealand flux research and monitoring.
**Download:** https://www.ozflux.org.au/data.html

---

## DATASET 46: Physical Activity & Health (NHANES)
**Domain:** Exercise Physiology, Public Health, Nutritional Physiology
**Source:** CDC NHANES — https://www.cdc.gov/nchs/nhanes/
**Format:** CSV
**Rows:** 50,000+ participants, 500+ health and lifestyle attributes
**Target:** BMI / cardiovascular risk / diabetes
**ML Tasks:** Regression, classification, clustering
**Citation:** CDC. National Health and Nutrition Examination Survey.
**Download:** https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/default.aspx

---

## DATASET 47: Palaeontology — Fossil Occurrences (PBDB)
**Domain:** Palaeontology, Evolutionary Biology
**Source:** Paleobiology Database — https://paleobiodb.org/
**Format:** CSV
**Rows:** 1,000,000+ fossil occurrence records (global)
**Target:** Extinction risk / taxonomic classification
**ML Tasks:** Classification, time series, phylogenetic analysis
**Citation:** The Paleobiology Database.
**Download:** https://paleobiodb.org/data1.2/occs/list.csv?datainfo&rowcount&show=full

---

## DATASET 48: Package Delivery Route Optimization
**Domain:** Packaging, Storage, Transportation, Logistics
**Source:** Kaggle — https://www.kaggle.com/datasets/ub11321/route-optimization-dataset
**Format:** CSV
**Rows:** 100,000+ delivery route records, 20+ features
**Target:** Delivery time / route efficiency
**ML Tasks:** Regression, optimization, time series
**Citation:** Route Optimization dataset. Kaggle.
**Download:** https://www.kaggle.com/datasets/ub11321/route-optimization-dataset

---

## DATASET 49: Autoimmune Disease (Lupus Gene Expression)
**Domain:** Autoimmunity, Immunology, Genetic Immunology
**Source:** NCBI GEO — https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE65391
**Format:** CSV
**Rows:** 1,200+ gene expression samples, 50,000+ probes
**Target:** Lupus vs Healthy
**ML Tasks:** Binary classification, biomarker discovery
**Citation:** GEO. Gene expression in systemic lupus erythematosus.
**Download:** https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE65391

---

## DATASET 50: Education Policy — PISA Global Scores
**Domain:** Public Policy, Education Assessment, Educational Admin
**Source:** OECD PISA — https://www.oecd.org/pisa/
**Format:** CSV
**Rows:** 600,000+ student scores across 80+ countries (triennial)
**Target:** Math/Reading/Science scores
**ML Tasks:** Regression, clustering, policy analysis
**Citation:** OECD. PISA (Programme for International Student Assessment).
**Download:** https://www.oecd.org/pisa/data/

---

## DATASET 51: Soil Moisture Prediction (Australian Sites)
**Domain:** Soil Sciences, Geomorphology, Water Resources
**Source:** CSIRO / Terrestrial Ecosystem Research Network — https://www.tern.org.au/
**Format:** CSV
**Rows:** 100,000+ soil moisture readings from Australian monitoring sites
**Target:** Soil moisture content (%)
**ML Tasks:** Regression, time series, environmental modelling
**Citation:** TERN. Australian Soil Moisture Monitoring Network.
**Download:** https://www.tern.org.au/soil-moisture-data/

---

## DATASET 52: Tumour Immunology — Immunotherapy Responses
**Domain:** Tumour Immunology, Transplantation Immunology, Oncology
**Source:** NCBI GEO — https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE91061
**Format:** CSV
**Rows:** 2,000+ tumour samples with immune infiltration data
**Target:** Immunotherapy response (responder vs non-responder)
**ML Tasks:** Binary classification, biomarker discovery
**Citation:** GEO. Immunotherapy response in melanoma patients.
**Download:** https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE91061

---

## DATASET 53: Global Change — Land Use Change (Australia)
**Domain:** Global Change Biology, Land Use Planning, Environmental Management
**Source:** data.gov.au / NSW Land Use — https://datasets.seed.nsw.gov.au/dataset/nsw-land-use
**Format:** CSV / Shapefile
**Rows:** 500,000+ land parcels with land use classification (1990-2020)
**Target:** Land use category / change detection
**ML Tasks:** Multi-class classification, change detection, spatial analysis
**Citation:** NSW Department of Planning. Land Use dataset.
**Download:** https://datasets.seed.nsw.gov.au/dataset/nsw-land-use

---

## DATASET 54: Crop Protection — Pest Infestation (Australian Wheat)
**Domain:** Crop and Pasture Protection, Agriculture, Microbiology
**Source:** data.gov.au / DAFF — https://www.agriculture.gov.au/biosecurity-trade
**Format:** CSV
**Rows:** 10,000+ pest infestation records across Australian crop regions
**Target:** Pest type / infestation severity
**ML Tasks:** Multi-class classification, risk prediction
**Citation:** Australian Department of Agriculture. Plant Pest Database.
**Download:** https://www.agriculture.gov.au/biosecurity-trade

---

## DATASET 55: Microbial Genetics — Antibiotic Resistance (AMR)
**Domain:** Microbial Genetics, Microbiology, Genetics
**Source:** NCBI / Pathogen Detection — https://www.ncbi.nlm.nih.gov/pathogens/
**Format:** CSV
**Rows:** 500,000+ bacterial isolates with resistance phenotypes
**Target:** Antibiotic resistance (resistant vs susceptible)
**ML Tasks:** Binary classification, genomic prediction
**Citation:** NCBI Pathogen Detection. Isolates Browser.
**Download:** https://www.ncbi.nlm.nih.gov/pathogens/isolates/

---

## DATASET 56: Sports Medicine — ACL Injury Prediction
**Domain:** Sports Medicine, Exercise Physiology
**Source:** Kaggle — https://www.kaggle.com/datasets/axoner/acl-injury-prediction
**Format:** CSV
**Rows:** 5,000+ athlete biomechanical records
**Target:** ACL injury risk (high vs low)
**ML Tasks:** Binary classification, risk prediction
**Citation:** ACL Injury Prediction Dataset. Kaggle.
**Download:** https://www.kaggle.com/datasets/axoner/acl-injury-prediction

---

## DATASET 57: Bioinformatics — Protein Sequence Classification
**Domain:** Bioinformatics, Computational Biology
**Source:** UCI ML Repository — https://archive.ics.uci.edu/ml/datasets/Molecular+Biology+(Protein+Secondary+Structure)
**Format:** CSV / Text
**Rows:** 15,000+ protein sequences with structural annotations
**Target:** Secondary structure element (Helix/Sheet/Coil)
**ML Tasks:** Sequence classification, bioinformatics
**Citation:** Qian, N., & Sejnowski, T. J. (1988). Predicting the secondary structure of globular proteins using neural network models.
**Download:** https://archive.ics.uci.edu/static/public/82/molecular+biology+protein+secondary+structure.zip

---

## DATASET 58: Health Informatics — Hospital Readmission (All Causes)
**Domain:** Health Informatics, Mental Health Services, Medicine
**Source:** UCI ML Repository — https://archive.ics.uci.edu/ml/datasets/Diabetes+130-US+hospitals+for+years+1999-2008
**Format:** CSV
**Rows:** 101,766 hospital readmission records
**Target:** Readmission prediction (<30 days)
**ML Tasks:** Binary classification, health analytics
**Citation:** Strack, B., et al. (2014). Impact of HbA1c on hospital readmission.
**Download:** https://archive.ics.uci.edu/static/public/296/diabetes+130+us+hospitals+for+years+1999+2008.zip

---

## DATASET 59: Climate Adaptation — Australian Bushfire Risk
**Domain:** Climate Change Adaptation, Climate Science, Emergency Management
**Source:** data.gov.au / Bushfire & Natural Haz CRC — https://www.bnhcrc.com.au/
**Format:** CSV
**Rows:** 50,000+ historical bushfire records with climate variables
**Target:** Fire danger rating / ignition risk
**ML Tasks:** Classification, risk prediction, time series
**Citation:** BNHCRC. Bushfire risk modelling datasets.
**Download:** https://www.bnhcrc.com.au/hazardnotes/data

---

## DATASET 60: NLP — Mental Health (Depression Detection)
**Domain:** Language, Mental Health Services, NLP
**Source:** Kaggle — https://www.kaggle.com/datasets/saurabhshahane/depression-detection-dataset
**Format:** CSV (text)
**Rows:** 40,000+ social media posts labelled for depression indicators
**Target:** Depression vs Control
**ML Tasks:** NLP binary classification, sentiment analysis
**Citation:** Depression Detection Dataset. Kaggle.
**Download:** https://www.kaggle.com/datasets/saurabhshahane/depression-detection-dataset

---

## MASTER TABLE (60 Datasets)

| # | Dataset | Domain | Rows | ML Task | Format | Source |
|---|---------|--------|:----:|---------|--------|--------|
| 1 | Heart Disease | Medicine | 303 | Classification | CSV | UCI |
| 2 | Gene Expression Cancer | Cancer/Genomics | 801 | Classification | CSV | UCI |
| 3 | Earth Surface Temperature | Climate Science | 8.5M | Time Series | CSV | Kaggle |
| 4 | Wine Quality | Chemistry | 4,898 | Regression | CSV | UCI |
| 5 | Mushroom Classification | Mycology | 8,124 | Classification | CSV | UCI |
| 6 | Epileptic Seizure | Neuroscience | 11,500 | Classification | CSV | UCI |
| 7 | Dengue Cases | Infectious Diseases | 1,456 | Regression | CSV | DrivenData |
| 8 | Breast Cancer | Cancer | 569 | Classification | CSV | UCI |
| 9 | E. coli Proteins | Cell Biology | 336 | Classification | CSV | UCI |
| 10 | Handwritten Digits | Computer Vision | 7,400 | Classification | CSV | UCI |
| 11 | Adult Census Income | Sociology | 48,842 | Classification | CSV | UCI |
| 12 | Drug Reviews | Pharmacology | 215,063 | NLP | TSV | UCI |
| 13 | Human Activity | Biophysics | 10,299 | Classification | CSV | UCI |
| 14 | Forest Cover Type | Ecology | 581,012 | Classification | CSV | UCI |
| 15 | Protein Structure | Biochemistry | 45,730 | Regression | CSV | UCI |
| 16 | Cyberbullying | Psychology | 47,000 | NLP | CSV | Kaggle |
| 17 | Diabetic Retinopathy | Medicine | 35,126 | Image Classif | Images | Kaggle |
| 18 | Australian Tourism | Sociology/Econ | 10,000+ | Forecasting | CSV | data.gov.au |
| 19 | Beachwatch Water Quality | Oceanography | 50,000+ | Classification | CSV | data.nsw.gov.au |
| 20 | DNA Gene Sequences | Genomics | 10K+ | Classification | CSV | Kaggle |
| 21 | Beijing Air Quality | Environmental Eng | 43,824 | Regression | CSV | UCI |
| 22 | DNA Methylation | Epigenetics/Cancer | 96 samples | Classification | CSV | NCBI |
| 23 | EEG Brainwave | Neurology | 14,980 | Classification | CSV | UCI |
| 24 | Food Nutrition | Food Chemistry | 7,800+ | Classification | CSV | USDA |
| 25 | Chest X-Ray | Radiology | 5,863 | Image Classif | Images | Kaggle |
| 26 | Diabetes Readmission | Geriatrics | 101,766 | Classification | CSV | UCI |
| 27 | Species Distribution | Ecology | 1M+ | Classification | CSV | GBIF |
| 28 | Liver Disease | Gastroenterology | 583 | Classification | CSV | UCI |
| 29 | Crop Yields | Agriculture | 80,000+ | Regression | CSV | OWID |
| 30 | Gene Therapy Vectors | Gene Therapy | 5,000+ | Regression | CSV | AddGene |
| 31 | Forest Fires | Forestry | 517 | Regression | CSV | UCI |
| 32 | Chronic Kidney Disease | Nephrology | 400 | Classification | CSV | UCI |
| 33 | Dermatology | Dermatology | 366 | Classification | CSV | UCI |
| 34 | Uterine Cancer | Oncology | 350 | Classification | CSV | UCI |
| 35 | Water Potability | Freshwater Ecology | 3,276 | Classification | CSV | Kaggle |
| 36 | Fitbit Athlete Activity | Sports Nutrition | 33,000 | Regression | CSV | Kaggle |
| 37 | MIMIC-III ICU | Emergency Medicine | 53,423 | Classification | CSV | PhysioNet |
| 38 | Thyroid Disease | Endocrinology | 7,200 | Classification | CSV | UCI |
| 39 | Foodborne Illness | Food Safety | 50,000 | Classification | CSV | CDC |
| 40 | Australian Rainfall | Climatology | 100K+ | Forecasting | CSV | BOM |
| 41 | Wine Quality (Vinho Verde) | Oenology | 4,898 | Regression | CSV | UCI |
| 42 | Cervical Cancer Risk | Oncology | 858 | Classification | CSV | UCI |
| 43 | Kangaroo Tracking | Wildlife | 50K+ | Classification | CSV | ALA |
| 44 | Student Performance | Education | 1,044 | Regression | CSV | UCI |
| 45 | Carbon Flux (OzFlux) | Climate | 500K+ | Regression | CSV | OzFlux |
| 46 | NHANES Health Survey | Public Health | 50K+ | Regression | CSV | CDC |
| 47 | Fossil Occurrences | Palaeontology | 1M+ | Classification | CSV | PBDB |
| 48 | Route Optimization | Logistics | 100K+ | Regression | CSV | Kaggle |
| 49 | Lupus Gene Expression | Immunology | 1,200 | Classification | CSV | GEO |
| 50 | PISA Global Scores | Education | 600K+ | Regression | CSV | OECD |
| 51 | Soil Moisture (Aus) | Soil Sciences | 100K+ | Regression | CSV | TERN |
| 52 | Tumour Immunotherapy | Immunology | 2,000 | Classification | CSV | GEO |
| 53 | Land Use Change (NSW) | Land Use Planning | 500K+ | Classification | CSV | SEED |
| 54 | Crop Pest Infestation | Agriculture | 10K+ | Classification | CSV | DAFF |
| 55 | Antibiotic Resistance (AMR) | Microbial Genetics | 500K+ | Classification | CSV | NCBI |
| 56 | ACL Injury Prediction | Sports Medicine | 5,000+ | Classification | CSV | Kaggle |
| 57 | Protein Sequence (Bioinfo) | Bioinformatics | 15K+ | Classification | CSV | UCI |
| 58 | Hospital Readmission | Health Informatics | 101K+ | Classification | CSV | UCI |
| 59 | Bushfire Risk (Aus) | Climate Adaptation | 50K+ | Classification | CSV | BNHCRC |
| 60 | Depression Detection (NLP) | Mental Health / NLP | 40K+ | NLP | CSV | Kaggle |
