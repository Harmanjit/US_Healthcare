DB: /Users/harman/Documents/GitHub/US_Healthcare/raw/armd.sqlite
Tables: 16

========================================================================================
TABLE: implied_susceptibility_rules
Rows:  50
Cols:  3
Schema: Organism, Antibiotic, Rule

Column stats (null/empty, distinct):
- Organism: null/empty=0 distinct=8
- Antibiotic: null/empty=0 distinct=20
- Rule: null/empty=0 distinct=11

Sample (first 5 rows; showing up to 3 cols):
- row 1: Organism='ACINETOBACTER', Antibiotic='Aztreonam', Rule='Resistant'
- row 2: Organism='ACINETOBACTER', Antibiotic='Cefazolin', Rule='Resistant'
- row 3: Organism='ACINETOBACTER', Antibiotic='Minocycline', Rule='Resistant'
- row 4: Organism='ACINETOBACTER', Antibiotic='Tetracycline', Rule='Resistant'
- row 5: Organism='ACINETOBACTER', Antibiotic='Doripenem', Rule='Same as Meropenem if reported'

========================================================================================
TABLE: microbiology_culture_prior_infecting_organism
Rows:  1,083,739
Cols:  6
Schema: anon_id, pat_enc_csn_id_coded, order_proc_id_coded, order_time_jittered_utc, prior_organism, prior_infecting_organism_days_to_culutre

Column stats (null/empty, distinct):
- anon_id: null/empty=0 distinct=45,499
- pat_enc_csn_id_coded: null/empty=0 distinct=157,645
- order_proc_id_coded: null/empty=0 distinct=209,723
- order_time_jittered_utc: null/empty=0 distinct=156,251
- prior_organism: null/empty=0 distinct=16
- prior_infecting_organism_days_to_culutre: null/empty=0 distinct=5,663

Sample (first 5 rows; showing up to 6 cols):
- row 1: anon_id='JC1000055', pat_enc_csn_id_coded='131007833415', order_proc_id_coded='360359154', order_time_jittered_utc='2009-11-27 02:52:00+00:00', prior_organism='Escherichia', prior_infecting_organism_days_to_culutre='40'
- row 2: anon_id='JC1000080', pat_enc_csn_id_coded='131270202433', order_proc_id_coded='615165101', order_time_jittered_utc='2019-07-19 22:51:00+00:00', prior_organism='Escherichia', prior_infecting_organism_days_to_culutre='2361'
- row 3: anon_id='JC1000083', pat_enc_csn_id_coded='131013906068', order_proc_id_coded='384652929', order_time_jittered_utc='2011-06-18 00:10:00+00:00', prior_organism='Staphylococcus', prior_infecting_organism_days_to_culutre='30'
- row 4: anon_id='JC1000129', pat_enc_csn_id_coded='131354606122', order_proc_id_coded='876959985', order_time_jittered_utc='2023-04-23 22:44:00+00:00', prior_organism='Escherichia', prior_infecting_organism_days_to_culutre='91'
- row 5: anon_id='JC1000129', pat_enc_csn_id_coded='131354606122', order_proc_id_coded='876959985', order_time_jittered_utc='2023-04-23 22:44:00+00:00', prior_organism='Escherichia', prior_infecting_organism_days_to_culutre='115'

========================================================================================
TABLE: microbiology_cultures_adi_scores
Rows:  751,075
Cols:  6
Schema: anon_id, pat_enc_csn_id_coded, order_proc_id_coded, order_time_jittered_utc, adi_score, adi_state_rank

Column stats (null/empty, distinct):
- anon_id: null/empty=0 distinct=283,715
- pat_enc_csn_id_coded: null/empty=0 distinct=574,584
- order_proc_id_coded: null/empty=0 distinct=751,075
- order_time_jittered_utc: null/empty=0 distinct=539,681
- adi_score: null/empty=0 distinct=101
- adi_state_rank: null/empty=0 distinct=11

Sample (first 5 rows; showing up to 6 cols):
- row 1: anon_id='JC6213422', pat_enc_csn_id_coded='131321523364', order_proc_id_coded='759748723', order_time_jittered_utc='2021-11-19 08:30:00+00:00', adi_score='Null', adi_state_rank='Null'
- row 2: anon_id='JC6298763', pat_enc_csn_id_coded='131361363555', order_proc_id_coded='902110506', order_time_jittered_utc='2023-09-30 20:18:00+00:00', adi_score='Null', adi_state_rank='Null'
- row 3: anon_id='JC6272591', pat_enc_csn_id_coded='131340198255', order_proc_id_coded='818636183', order_time_jittered_utc='2022-10-05 03:27:00+00:00', adi_score='Null', adi_state_rank='Null'
- row 4: anon_id='JC1317627', pat_enc_csn_id_coded='131017484560', order_proc_id_coded='396745616', order_time_jittered_utc='2012-01-26 02:04:00+00:00', adi_score='Null', adi_state_rank='Null'
- row 5: anon_id='JC1523941', pat_enc_csn_id_coded='131020403526', order_proc_id_coded='406388185', order_time_jittered_utc='2012-09-10 03:22:00+00:00', adi_score='Null', adi_state_rank='Null'

========================================================================================
TABLE: microbiology_cultures_antibiotic_class_exposure
Rows:  5,402,486
Cols:  8
Schema: anon_id, pat_enc_csn_id_coded, order_proc_id_coded, order_time_jittered_utc, medication_category, medication_name, antibiotic_class, time_to_culturetime

Column stats (null/empty, distinct):
- anon_id: null/empty=0 distinct=153,555
- pat_enc_csn_id_coded: null/empty=0 distinct=365,226
- order_proc_id_coded: null/empty=0 distinct=484,370
- order_time_jittered_utc: null/empty=0 distinct=345,816
- medication_category: null/empty=0 distinct=89
- medication_name: null/empty=0 distinct=89
- antibiotic_class: null/empty=0 distinct=18
- time_to_culturetime: null/empty=0 distinct=5,672

Sample (first 5 rows; showing up to 8 cols):
- row 1: anon_id='JC600474', pat_enc_csn_id_coded='131332758707', order_proc_id_coded='794295244', order_time_jittered_utc='2022-05-13 16:38:00+00:00', medication_category='RIF1', medication_name='Rifampin', antibiotic_class='Ansamycin', time_to_culturetime='993'
- row 2: anon_id='JC989728', pat_enc_csn_id_coded='131146201135', order_proc_id_coded='484084816', order_time_jittered_utc='2016-02-02 01:54:00+00:00', medication_category='RIF1', medication_name='Rifampin', antibiotic_class='Ansamycin', time_to_culturetime='55'
- row 3: anon_id='JC680296', pat_enc_csn_id_coded='131309701100', order_proc_id_coded='736813810', order_time_jittered_utc='2021-07-25 23:37:00+00:00', medication_category='RIF1', medication_name='Rifampin', antibiotic_class='Ansamycin', time_to_culturetime='1829'
- row 4: anon_id='JC2740316', pat_enc_csn_id_coded='131304422274', order_proc_id_coded='718374179', order_time_jittered_utc='2021-03-19 19:18:00+00:00', medication_category='RIF1', medication_name='Rifampin', antibiotic_class='Ansamycin', time_to_culturetime='192'
- row 5: anon_id='JC1624219', pat_enc_csn_id_coded='131355262042', order_proc_id_coded='880563445', order_time_jittered_utc='2023-06-27 09:02:00+00:00', medication_category='RIF1', medication_name='Rifampin', antibiotic_class='Ansamycin', time_to_culturetime='3450'

========================================================================================
TABLE: microbiology_cultures_antibiotic_subtype_exposure
Rows:  5,402,486
Cols:  9
Schema: anon_id, pat_enc_csn_id_coded, order_proc_id_coded, order_time_jittered_utc, medication_category, medication_name, antibiotic_subtype, antibiotic_subtype_category, medication_time_to_cultureTime

Column stats (null/empty, distinct):
- anon_id: null/empty=0 distinct=153,555
- pat_enc_csn_id_coded: null/empty=0 distinct=365,226
- order_proc_id_coded: null/empty=0 distinct=484,370
- order_time_jittered_utc: null/empty=0 distinct=345,816
- medication_category: null/empty=0 distinct=89
- medication_name: null/empty=0 distinct=89
- antibiotic_subtype: null/empty=0 distinct=25
- antibiotic_subtype_category: null/empty=0 distinct=25
- medication_time_to_cultureTime: null/empty=0 distinct=5,672

Sample (first 5 rows; showing up to 8 cols):
- row 1: anon_id='JC661393', pat_enc_csn_id_coded='131323239770', order_proc_id_coded='764294462', order_time_jittered_utc='2021-12-11 00:00:00+00:00', medication_category='RIF2', medication_name='Rifabutin', antibiotic_subtype='Ansamycin', antibiotic_subtype_category='ANS'
- row 2: anon_id='JC2160561', pat_enc_csn_id_coded='131338576141', order_proc_id_coded='825909791', order_time_jittered_utc='2022-11-09 22:15:00+00:00', medication_category='RIF2', medication_name='Rifabutin', antibiotic_subtype='Ansamycin', antibiotic_subtype_category='ANS'
- row 3: anon_id='JC2934880', pat_enc_csn_id_coded='131343502227', order_proc_id_coded='830405835', order_time_jittered_utc='2022-11-03 20:52:00+00:00', medication_category='RIF2', medication_name='Rifabutin', antibiotic_subtype='Ansamycin', antibiotic_subtype_category='ANS'
- row 4: anon_id='JC902549', pat_enc_csn_id_coded='131312194725', order_proc_id_coded='730129849', order_time_jittered_utc='2021-05-27 20:12:00+00:00', medication_category='RIF2', medication_name='Rifabutin', antibiotic_subtype='Ansamycin', antibiotic_subtype_category='ANS'
- row 5: anon_id='JC881542', pat_enc_csn_id_coded='131042033458', order_proc_id_coded='446700182', order_time_jittered_utc='2014-09-18 18:54:00+00:00', medication_category='SIL', medication_name='Silver Sulfadiazine', antibiotic_subtype='Sulfonamide', antibiotic_subtype_category='SUL'

========================================================================================
TABLE: microbiology_cultures_cohort
Rows:  2,241,050
Cols:  10
Schema: anon_id, pat_enc_csn_id_coded, order_proc_id_coded, order_time_jittered_utc, ordering_mode, culture_description, was_positive, organism, antibiotic, susceptibility

Column stats (null/empty, distinct):
- anon_id: null/empty=0 distinct=283,715
- pat_enc_csn_id_coded: null/empty=0 distinct=574,584
- order_proc_id_coded: null/empty=0 distinct=751,075
- order_time_jittered_utc: null/empty=0 distinct=539,681
- ordering_mode: null/empty=0 distinct=3
- culture_description: null/empty=0 distinct=3
- was_positive: null/empty=0 distinct=2
- organism: null/empty=0 distinct=315
- antibiotic: null/empty=0 distinct=55
- susceptibility: null/empty=0 distinct=6

Sample (first 5 rows; showing up to 8 cols):
- row 1: anon_id='JC2744063', pat_enc_csn_id_coded='131368600230', order_proc_id_coded='928257722', order_time_jittered_utc='2023-12-23 22:29:00+00:00', ordering_mode='Inpatient', culture_description='URINE', was_positive='1', organism='KLEBSIELLA PNEUMONIAE'
- row 2: anon_id='JC1713666', pat_enc_csn_id_coded='131300064625', order_proc_id_coded='697566032', order_time_jittered_utc='2020-12-27 00:40:00+00:00', ordering_mode='Inpatient', culture_description='URINE', was_positive='1', organism='KLEBSIELLA PNEUMONIAE'
- row 3: anon_id='JC1669304', pat_enc_csn_id_coded='131272997044', order_proc_id_coded='620809641', order_time_jittered_utc='2019-07-02 19:54:00+00:00', ordering_mode='Inpatient', culture_description='BLOOD', was_positive='1', organism='KLEBSIELLA PNEUMONIAE'
- row 4: anon_id='JC1697441', pat_enc_csn_id_coded='131208305006', order_proc_id_coded='510635146', order_time_jittered_utc='2016-12-01 13:59:00+00:00', ordering_mode='Inpatient', culture_description='URINE', was_positive='1', organism='KLEBSIELLA PNEUMONIAE'
- row 5: anon_id='JC600786', pat_enc_csn_id_coded='131344486993', order_proc_id_coded='834128837', order_time_jittered_utc='2022-11-18 19:35:00+00:00', ordering_mode='Outpatient', culture_description='URINE', was_positive='1', organism='KLEBSIELLA PNEUMONIAE'

========================================================================================
TABLE: microbiology_cultures_comorbidity
Rows:  206,547,140
Cols:  7
Schema: anon_id, pat_enc_csn_id_coded, order_proc_id_coded, order_time_jittered_utc, comorbidity_component, comorbidity_component_start_days_culture, comorbidity_component_end_days_culture

Column stats (null/empty, distinct):
- anon_id: null/empty=0 distinct=278,670
- pat_enc_csn_id_coded: null/empty=0 distinct=563,100
- order_proc_id_coded: null/empty=0 distinct=733,149
- order_time_jittered_utc: null/empty=0 distinct=524,727
- comorbidity_component: null/empty=6,954 distinct=519
- comorbidity_component_start_days_culture: null/empty=6,954 distinct=8,305
- comorbidity_component_end_days_culture: null/empty=203,436,770 distinct=10,215

Sample (first 5 rows; showing up to 7 cols):
- row 1: anon_id='JC606511', pat_enc_csn_id_coded='131258041213', order_proc_id_coded='578613947', order_time_jittered_utc='2018-10-26 22:02:00+00:00', comorbidity_component='Glaucoma', comorbidity_component_start_days_culture='2410', comorbidity_component_end_days_culture=''
- row 2: anon_id='JC960669', pat_enc_csn_id_coded='131276316369', order_proc_id_coded='631567748', order_time_jittered_utc='2019-10-16 07:00:00+00:00', comorbidity_component='Other specified and unspecified upper respiratory disease', comorbidity_component_start_days_culture='227', comorbidity_component_end_days_culture=''
- row 3: anon_id='JC835033', pat_enc_csn_id_coded='131367931012', order_proc_id_coded='925529804', order_time_jittered_utc='2024-01-14 16:51:00+00:00', comorbidity_component='Conduction disorders', comorbidity_component_start_days_culture='5698', comorbidity_component_end_days_culture=''
- row 4: anon_id='JC1424164', pat_enc_csn_id_coded='131284461772', order_proc_id_coded='655912284', order_time_jittered_utc='2020-02-05 23:28:00+00:00', comorbidity_component='Hearing loss', comorbidity_component_start_days_culture='981', comorbidity_component_end_days_culture=''
- row 5: anon_id='JC2107178', pat_enc_csn_id_coded='131297185672', order_proc_id_coded='688900777', order_time_jittered_utc='2020-11-24 06:43:00+00:00', comorbidity_component='Respiratory failure; insufficiency; arrest', comorbidity_component_start_days_culture='22', comorbidity_component_end_days_culture=''

========================================================================================
TABLE: microbiology_cultures_demographics
Rows:  751,075
Cols:  5
Schema: anon_id, pat_enc_csn_id_coded, order_proc_id_coded, age, gender

Column stats (null/empty, distinct):
- anon_id: null/empty=0 distinct=283,715
- pat_enc_csn_id_coded: null/empty=0 distinct=574,584
- order_proc_id_coded: null/empty=0 distinct=751,075
- age: null/empty=0 distinct=9
- gender: null/empty=0 distinct=3

Sample (first 5 rows; showing up to 5 cols):
- row 1: anon_id='JC1212710', pat_enc_csn_id_coded='131008781669', order_proc_id_coded='364609652', age='25-34 years', gender='Null'
- row 2: anon_id='JC1218441', pat_enc_csn_id_coded='33052060', order_proc_id_coded='351667304', age='25-34 years', gender='Null'
- row 3: anon_id='JC1261412', pat_enc_csn_id_coded='131004002288', order_proc_id_coded='355531114', age='25-34 years', gender='Null'
- row 4: anon_id='JC1224853', pat_enc_csn_id_coded='19532426', order_proc_id_coded='335118697', age='25-34 years', gender='Null'
- row 5: anon_id='JC1242725', pat_enc_csn_id_coded='32587123', order_proc_id_coded='349578403', age='25-34 years', gender='Null'

========================================================================================
TABLE: microbiology_cultures_implied_susceptibility
Rows:  1,978,731
Cols:  7
Schema: anon_id, pat_enc_csn_id_coded, order_proc_id_coded, organism, antibiotic, susceptibility, implied_susceptibility

Column stats (null/empty, distinct):
- anon_id: null/empty=0 distinct=67,010
- pat_enc_csn_id_coded: null/empty=0 distinct=117,014
- order_proc_id_coded: null/empty=0 distinct=118,763
- organism: null/empty=0 distinct=313
- antibiotic: null/empty=0 distinct=69
- susceptibility: null/empty=0 distinct=14
- implied_susceptibility: null/empty=0 distinct=3

Sample (first 5 rows; showing up to 7 cols):
- row 1: anon_id='JC2673551', pat_enc_csn_id_coded='131337997983', order_proc_id_coded='831009441', organism='ENTEROBACTER CLOACAE COMPLEX', antibiotic='imipenem', susceptibility='Null', implied_susceptibility='Susceptible'
- row 2: anon_id='JC616267', pat_enc_csn_id_coded='131007285560', order_proc_id_coded='358749950', organism='ENTEROBACTER CLOACAE', antibiotic='imipenem', susceptibility='Null', implied_susceptibility='Null'
- row 3: anon_id='JC517471', pat_enc_csn_id_coded='131024758159', order_proc_id_coded='420255585', organism='ENTEROBACTER ASBURIAE', antibiotic='doripenem', susceptibility='Null', implied_susceptibility='Null'
- row 4: anon_id='JC1931399', pat_enc_csn_id_coded='131200817434', order_proc_id_coded='512398445', organism='MYCOBACTERIUM AVIUM COMPLEX', antibiotic='Clarithromycin', susceptibility='Susceptible', implied_susceptibility='Null'
- row 5: anon_id='JC605042', pat_enc_csn_id_coded='131280233261', order_proc_id_coded='642349435', organism='KLEBSIELLA OXYTOCA', antibiotic='Ceftolozane/Tazobactam', susceptibility='Susceptible', implied_susceptibility='Null'

========================================================================================
TABLE: microbiology_cultures_labs
Rows:  1,408,677
Cols:  59
Schema: anon_id, pat_enc_csn_id_coded, order_proc_id_coded, Period_Day, Q75_wbc, Q25_wbc, median_wbc, Q25_neutrophils, Q75_neutrophils, median_neutrophils, Q25_lymphocytes, Q75_lymphocytes ...

Column stats (null/empty, distinct):
- anon_id: null/empty=0 distinct=197,305
- pat_enc_csn_id_coded: null/empty=0 distinct=335,284
- order_proc_id_coded: null/empty=0 distinct=492,659
- Period_Day: null/empty=0 distinct=1
- Q75_wbc: null/empty=0 distinct=1,471
- Q25_wbc: null/empty=0 distinct=1,260
- median_wbc: null/empty=0 distinct=1,345
- Q25_neutrophils: null/empty=0 distinct=893
- Q75_neutrophils: null/empty=0 distinct=925
- median_neutrophils: null/empty=0 distinct=914
- Q25_lymphocytes: null/empty=0 distinct=702
- Q75_lymphocytes: null/empty=0 distinct=819
- median_lymphocytes: null/empty=0 distinct=735
- Q25_hgb: null/empty=0 distinct=196
- Q75_hgb: null/empty=0 distinct=196
- median_hgb: null/empty=0 distinct=193
- Q25_plt: null/empty=0 distinct=1,046
- Q75_plt: null/empty=0 distinct=1,169
- median_plt: null/empty=0 distinct=1,078
- Q75_na: null/empty=0 distinct=78
- Q25_na: null/empty=0 distinct=79
- median_na: null/empty=0 distinct=79
- Q75_hco3: null/empty=0 distinct=273
- Q25_hco3: null/empty=0 distinct=258
- median_hco3: null/empty=0 distinct=255
(skipped 34 columns; use --max-stat-cols to change)

Sample (first 5 rows; showing up to 8 cols):
- row 1: anon_id='JC3080045', pat_enc_csn_id_coded='131362484007', order_proc_id_coded='906727631', Period_Day='14', Q75_wbc='Null', Q25_wbc='Null', median_wbc='Null', Q25_neutrophils='49.0'
- row 2: anon_id='JC2891328', pat_enc_csn_id_coded='131283209225', order_proc_id_coded='654338304', Period_Day='14', Q75_wbc='Null', Q25_wbc='Null', median_wbc='Null', Q25_neutrophils='29.0'
- row 3: anon_id='JC2761705', pat_enc_csn_id_coded='131279968565', order_proc_id_coded='645785381', Period_Day='14', Q75_wbc='Null', Q25_wbc='Null', median_wbc='Null', Q25_neutrophils='4.0'
- row 4: anon_id='JC1464815', pat_enc_csn_id_coded='131018095632', order_proc_id_coded='398734817', Period_Day='14', Q75_wbc='Null', Q25_wbc='Null', median_wbc='Null', Q25_neutrophils='58.0'
- row 5: anon_id='JC2004854', pat_enc_csn_id_coded='131358162167', order_proc_id_coded='902622534', Period_Day='14', Q75_wbc='Null', Q25_wbc='Null', median_wbc='Null', Q25_neutrophils='39.0'

========================================================================================
TABLE: microbiology_cultures_microbial_resistance
Rows:  2,161,648
Cols:  7
Schema: anon_id, pat_enc_csn_id_coded, order_proc_id_coded, order_time_jittered_utc, organism, antibiotic, resistant_time_to_culturetime

Column stats (null/empty, distinct):
- anon_id: null/empty=0 distinct=32,780
- pat_enc_csn_id_coded: null/empty=0 distinct=122,726
- order_proc_id_coded: null/empty=0 distinct=166,537
- order_time_jittered_utc: null/empty=0 distinct=122,245
- organism: null/empty=0 distinct=292
- antibiotic: null/empty=0 distinct=26
- resistant_time_to_culturetime: null/empty=0 distinct=5,615

Sample (first 5 rows; showing up to 7 cols):
- row 1: anon_id='JC1255618', pat_enc_csn_id_coded='131301644146', order_proc_id_coded='701878721', order_time_jittered_utc='2020-12-18 01:18:00+00:00', organism='MYCOBACTERIUM ABSCESSUS', antibiotic='Minocycline', resistant_time_to_culturetime='1266'
- row 2: anon_id='JC533377', pat_enc_csn_id_coded='131311775703', order_proc_id_coded='737610687', order_time_jittered_utc='2021-07-24 18:06:00+00:00', organism='KLEBSIELLA PNEUMONIAE', antibiotic='Ertapenem', resistant_time_to_culturetime='845'
- row 3: anon_id='JC669033', pat_enc_csn_id_coded='131207605914', order_proc_id_coded='517925931', order_time_jittered_utc='2017-01-30 23:31:00+00:00', organism='BURKHOLDERIA CEPACIA', antibiotic='Minocycline', resistant_time_to_culturetime='2231'
- row 4: anon_id='JC1017583', pat_enc_csn_id_coded='131254647220', order_proc_id_coded='570493265', order_time_jittered_utc='2018-08-03 02:00:00+00:00', organism='MYCOBACTERIUM IMMUNOGENUM', antibiotic='Linezolid', resistant_time_to_culturetime='812'
- row 5: anon_id='JC2465442', pat_enc_csn_id_coded='131016167664', order_proc_id_coded='392129591', order_time_jittered_utc='2011-12-18 16:21:00+00:00', organism='PSEUDOMONAS AERUGINOSA', antibiotic='Colistin', resistant_time_to_culturetime='210'

========================================================================================
TABLE: microbiology_cultures_nursing_home_visits
Rows:  7,628
Cols:  5
Schema: anon_id, pat_enc_csn_id_coded, order_proc_id_coded, order_time_jittered_utc, nursing_home_visit_culture

Column stats (null/empty, distinct):
- anon_id: null/empty=0 distinct=3,643
- pat_enc_csn_id_coded: null/empty=0 distinct=4,363
- order_proc_id_coded: null/empty=0 distinct=7,369
- order_time_jittered_utc: null/empty=0 distinct=4,448
- nursing_home_visit_culture: null/empty=0 distinct=61

Sample (first 5 rows; showing up to 5 cols):
- row 1: anon_id='JC1000492', pat_enc_csn_id_coded='131356383252', order_proc_id_coded='883656151', order_time_jittered_utc='2023-07-11 00:58:00+00:00', nursing_home_visit_culture='1'
- row 2: anon_id='JC1000492', pat_enc_csn_id_coded='131356383252', order_proc_id_coded='883656152', order_time_jittered_utc='2023-07-11 00:58:00+00:00', nursing_home_visit_culture='1'
- row 3: anon_id='JC1001762', pat_enc_csn_id_coded='131300824908', order_proc_id_coded='699593244', order_time_jittered_utc='2021-01-18 17:00:00+00:00', nursing_home_visit_culture='1'
- row 4: anon_id='JC1001762', pat_enc_csn_id_coded='131300824908', order_proc_id_coded='699593245', order_time_jittered_utc='2021-01-18 17:00:00+00:00', nursing_home_visit_culture='1'
- row 5: anon_id='JC1002167', pat_enc_csn_id_coded='131020983715', order_proc_id_coded='408363127', order_time_jittered_utc='2012-10-14 06:57:00+00:00', nursing_home_visit_culture='1'

========================================================================================
TABLE: microbiology_cultures_prior_med
Rows:  9,823,458
Cols:  7
Schema: anon_id, pat_enc_csn_id_coded, order_proc_id_coded, order_time_jittered_utc, medication_name, medication_time_to_culturetime, medication_category

Column stats (null/empty, distinct):
- anon_id: null/empty=0 distinct=196,564
- pat_enc_csn_id_coded: null/empty=0 distinct=430,625
- order_proc_id_coded: null/empty=0 distinct=575,344
- order_time_jittered_utc: null/empty=0 distinct=406,800
- medication_name: null/empty=0 distinct=89
- medication_time_to_culturetime: null/empty=0 distinct=5,673
- medication_category: null/empty=0 distinct=89

Sample (first 5 rows; showing up to 7 cols):
- row 1: anon_id='JC2106766', pat_enc_csn_id_coded='131237821282', order_proc_id_coded='534700983', order_time_jittered_utc='2017-08-14 22:40:00 UTC', medication_name='Sulfamethoxazole-Trimethoprim', medication_time_to_culturetime='90', medication_category='SUL'
- row 2: anon_id='JC2106766', pat_enc_csn_id_coded='131237821282', order_proc_id_coded='534700983', order_time_jittered_utc='2017-08-14 22:40:00 UTC', medication_name='Sulfamethoxazole-Trimethoprim', medication_time_to_culturetime='90', medication_category='SUL'
- row 3: anon_id='JC2106766', pat_enc_csn_id_coded='131237821282', order_proc_id_coded='534700983', order_time_jittered_utc='2017-08-14 22:40:00 UTC', medication_name='Levofloxacin In', medication_time_to_culturetime='91', medication_category='LEV1'
- row 4: anon_id='JC2106766', pat_enc_csn_id_coded='131237821282', order_proc_id_coded='534700983', order_time_jittered_utc='2017-08-14 22:40:00 UTC', medication_name='Vancomycin In Dextrose', medication_time_to_culturetime='92', medication_category='VAN1'
- row 5: anon_id='JC2106766', pat_enc_csn_id_coded='131237821282', order_proc_id_coded='534700983', order_time_jittered_utc='2017-08-14 22:40:00 UTC', medication_name='Vancomycin In Dextrose', medication_time_to_culturetime='92', medication_category='VAN1'

========================================================================================
TABLE: microbiology_cultures_priorprocedures
Rows:  1,664,615
Cols:  6
Schema: anon_id, pat_enc_csn_id_coded, order_proc_id_coded, order_time_jittered_utc, procedure_description, procedure_time_to_culturetime

Column stats (null/empty, distinct):
- anon_id: null/empty=0 distinct=68,253
- pat_enc_csn_id_coded: null/empty=0 distinct=171,240
- order_proc_id_coded: null/empty=0 distinct=251,759
- order_time_jittered_utc: null/empty=0 distinct=170,222
- procedure_description: null/empty=0 distinct=6
- procedure_time_to_culturetime: null/empty=0 distinct=5,420

Sample (first 5 rows; showing up to 6 cols):
- row 1: anon_id='JC1000129', pat_enc_csn_id_coded='131354606122', order_proc_id_coded='876959985', order_time_jittered_utc='2023-04-23 22:44:00+00:00', procedure_description='urethral_catheter', procedure_time_to_culturetime='126'
- row 2: anon_id='JC1000129', pat_enc_csn_id_coded='131359337847', order_proc_id_coded='894465321', order_time_jittered_utc='2023-07-12 23:05:00+00:00', procedure_description='urethral_catheter', procedure_time_to_culturetime='143'
- row 3: anon_id='JC1000589', pat_enc_csn_id_coded='131016666773', order_proc_id_coded='393806685', order_time_jittered_utc='2012-01-07 00:29:00+00:00', procedure_description='cvc', procedure_time_to_culturetime='378'
- row 4: anon_id='JC1000589', pat_enc_csn_id_coded='131018454256', order_proc_id_coded='400164900', order_time_jittered_utc='2012-05-14 20:44:00+00:00', procedure_description='cvc', procedure_time_to_culturetime='330'
- row 5: anon_id='JC1000589', pat_enc_csn_id_coded='131018454256', order_proc_id_coded='400164901', order_time_jittered_utc='2012-05-14 20:44:00+00:00', procedure_description='cvc', procedure_time_to_culturetime='507'

========================================================================================
TABLE: microbiology_cultures_vitals
Rows:  4,591,374
Cols:  28
Schema: anon_id, pat_enc_csn_id_coded, order_proc_id_coded, Q25_heartrate, Q75_heartrate, median_heartrate, Q25_resprate, Q75_resprate, median_resprate, Q25_temp, Q75_temp, median_temp ...

Column stats (null/empty, distinct):
- anon_id: null/empty=0 distinct=229,793
- pat_enc_csn_id_coded: null/empty=0 distinct=420,787
- order_proc_id_coded: null/empty=0 distinct=581,340
- Q25_heartrate: null/empty=0 distinct=167
- Q75_heartrate: null/empty=0 distinct=193
- median_heartrate: null/empty=0 distinct=171
- Q25_resprate: null/empty=0 distinct=54
- Q75_resprate: null/empty=0 distinct=60
- median_resprate: null/empty=0 distinct=56
- Q25_temp: null/empty=0 distinct=200
- Q75_temp: null/empty=0 distinct=213
- median_temp: null/empty=0 distinct=200
- Q25_sysbp: null/empty=0 distinct=200
- Q75_sysbp: null/empty=0 distinct=211
- median_sysbp: null/empty=0 distinct=204
- Q25_diasbp: null/empty=0 distinct=139
- Q75_diasbp: null/empty=0 distinct=170
- median_diasbp: null/empty=0 distinct=140
- first_diasbp: null/empty=0 distinct=152
- last_diasbp: null/empty=0 distinct=194
- last_sysbp: null/empty=0 distinct=236
- first_sysbp: null/empty=0 distinct=212
- last_temp: null/empty=0 distinct=255
- first_temp: null/empty=0 distinct=159
- last_resprate: null/empty=0 distinct=167
(skipped 3 columns; use --max-stat-cols to change)

Sample (first 5 rows; showing up to 8 cols):
- row 1: anon_id='JC2361817', pat_enc_csn_id_coded='131308278530', order_proc_id_coded='718222807', Q25_heartrate='86.0', Q75_heartrate='86.0', median_heartrate='86.0', Q25_resprate='Null', Q75_resprate='Null'
- row 2: anon_id='JC2219930', pat_enc_csn_id_coded='131318072067', order_proc_id_coded='748261410', Q25_heartrate='Null', Q75_heartrate='Null', median_heartrate='Null', Q25_resprate='Null', Q75_resprate='Null'
- row 3: anon_id='JC2455425', pat_enc_csn_id_coded='131256420868', order_proc_id_coded='574712812', Q25_heartrate='70.0', Q75_heartrate='70.0', median_heartrate='70.0', Q25_resprate='Null', Q75_resprate='Null'
- row 4: anon_id='JC1826078', pat_enc_csn_id_coded='131213257732', order_proc_id_coded='514463599', Q25_heartrate='Null', Q75_heartrate='Null', median_heartrate='Null', Q25_resprate='Null', Q75_resprate='Null'
- row 5: anon_id='JC1541734', pat_enc_csn_id_coded='131021676805', order_proc_id_coded='410407692', Q25_heartrate='39.0', Q75_heartrate='78.0', median_heartrate='73.0', Q25_resprate='Null', Q75_resprate='Null'

========================================================================================
TABLE: microbiology_cultures_ward_info
Rows:  751,075
Cols:  8
Schema: anon_id, pat_enc_csn_id_coded, order_proc_id_coded, order_time_jittered_utc, hosp_ward_IP, hosp_ward_OP, hosp_ward_ER, hosp_ward_ICU

Column stats (null/empty, distinct):
- anon_id: null/empty=0 distinct=283,715
- pat_enc_csn_id_coded: null/empty=0 distinct=574,584
- order_proc_id_coded: null/empty=0 distinct=751,075
- order_time_jittered_utc: null/empty=0 distinct=539,681
- hosp_ward_IP: null/empty=0 distinct=2
- hosp_ward_OP: null/empty=0 distinct=2
- hosp_ward_ER: null/empty=0 distinct=2
- hosp_ward_ICU: null/empty=0 distinct=2

Sample (first 5 rows; showing up to 8 cols):
- row 1: anon_id='JC1992981', pat_enc_csn_id_coded='131188197629', order_proc_id_coded='496076158', order_time_jittered_utc='2016-07-02 21:08:00+00:00', hosp_ward_IP='0', hosp_ward_OP='1', hosp_ward_ER='0', hosp_ward_ICU='0'
- row 2: anon_id='JC542594', pat_enc_csn_id_coded='15917502', order_proc_id_coded='327566424', order_time_jittered_utc='2008-07-16 03:23:00+00:00', hosp_ward_IP='0', hosp_ward_OP='1', hosp_ward_ER='0', hosp_ward_ICU='0'
- row 3: anon_id='JC597158', pat_enc_csn_id_coded='131276794493', order_proc_id_coded='642698667', order_time_jittered_utc='2019-11-10 22:54:00+00:00', hosp_ward_IP='0', hosp_ward_OP='1', hosp_ward_ER='0', hosp_ward_ICU='0'
- row 4: anon_id='JC1579203', pat_enc_csn_id_coded='131319187199', order_proc_id_coded='751697107', order_time_jittered_utc='2021-10-29 07:00:00+00:00', hosp_ward_IP='0', hosp_ward_OP='1', hosp_ward_ER='0', hosp_ward_ICU='0'
- row 5: anon_id='JC534140', pat_enc_csn_id_coded='131027275219', order_proc_id_coded='427106380', order_time_jittered_utc='2013-09-05 04:53:00+00:00', hosp_ward_IP='0', hosp_ward_OP='1', hosp_ward_ER='0', hosp_ward_ICU='0'