# Centre: Madhya Pradesh and Chhattisgarh with their neighbours.
# Executed inside timelines.py (ref() and timeline() are in scope).

ref('c_ciagency', 'Central India Agency', 'Wikipedia: created 1854 from the Western Malwa Agency and smaller offices; Gwalior placed under it the same year.', 'https://en.wikipedia.org/wiki/Central_India_Agency')
ref('c_gwaliorstate', 'Gwalior State', 'Wikipedia: Gwalior’s western boundary against Kotah, Jhalawar and Tonk of the Rajputana Agency, partly along the Chambal.', 'https://en.wikipedia.org/wiki/Gwalior_State')
ref('c_tonkstate', 'Tonk State', 'Wikipedia: six scattered districts, three (Tonk, Aligarh, Nimbahera) under the Rajputana Agency and three (Chhabra, Pirawa, Sironj) under the Central India Agency; acceded to India 7 April 1949.', 'https://en.wikipedia.org/wiki/Tonk_State')
ref('c_madhyabharat', 'Madhya Bharat', 'Wikipedia: the United State of Gwalior, Indore and Malwa, covenant signed 22 April 1948, inaugurated 28 May 1948.', 'https://en.wikipedia.org/wiki/Madhya_Bharat')
ref('c_vidisha', 'Vidisha district', 'Wikipedia: Bhilsa/Vidisha district’s formation, including the 1956 transfer of the Sironj tehsil (formerly part of Tonk State, then of Rajasthan’s Kota district) to Madhya Pradesh.', 'https://en.wikipedia.org/wiki/Vidisha_district')
ref('c_sunel', 'Sunel-Tappa', 'Wikipedia: a Madhya Bharat exclave of Mandsaur district’s Bhanpura tehsil, transferred to Rajasthan on 1 November 1956.', 'https://en.wikipedia.org/wiki/Sunel-Tappa')

ref('c_nagpurprov', 'Nagpur Province', 'Wikipedia: annexed by the British in 1853 under the doctrine of lapse; before 1861 it comprised the Nagpur Division, Chhindwara and Chhattisgarh.', 'https://en.wikipedia.org/wiki/Nagpur_Province')
ref('c_cp1861', 'Central Provinces', 'Wikipedia: formed in 1861 from Nagpur Province and the Saugor and Nerbudda Territories; contained a Marathi-speaking Vidarbha area in the south and a Hindi-speaking Mahakoshal in the north.', 'https://en.wikipedia.org/wiki/Central_Provinces')
ref('c_berarprovince', 'Berar Province', 'Wikipedia: the Hyderabad Assigned Districts, administered by the British from 1853 and permanently leased from the Nizam by the agreement of 5 November 1902.', 'https://en.wikipedia.org/wiki/Berar_Province')
ref('c_cpberar', 'Central Provinces and Berar', 'Wikipedia: Berar was merged administratively with the Central Provinces on 1 October 1903.', 'https://en.wikipedia.org/wiki/Central_Provinces_and_Berar')
ref('c_vidarbha', 'Vidarbha', 'Wikipedia: the Marathi-speaking Nagpur and Amravati (Berar) divisions were transferred from Madhya Pradesh to Bombay State in the 1956 reorganisation, then became part of Maharashtra under the Bombay Reorganisation Act, 1960.', 'https://en.wikipedia.org/wiki/Vidarbha')

timeline('Madhya Pradesh|Maharashtra',
    ('1853', 'Nagpur Province, ruled by the Bhonsle Rajas, is annexed by the British under the doctrine of lapse; it comprises the Marathi-speaking Nagpur Division as well as Chhindwara and Chhattisgarh.', ['c_nagpurprov']),
    ('1861', 'The Central Provinces are formed by merging Nagpur Province with the Saugor and Nerbudda Territories. The new province spans two linguistic zones: Marathi-speaking Vidarbha (the Nagpur division) in the south and Hindi-speaking Mahakoshal in the north, the future language line already running inside one province.', ['c_cp1861']),
    ('1902–03', 'Berar, the Hyderabad Assigned Districts administered by the British since 1853, is leased to Britain permanently by the Nizam’s agreement of 5 November 1902 and merged administratively with the Central Provinces on 1 October 1903 as Central Provinces and Berar, extending Marathi-speaking territory south of Nagpur.', ['c_berarprovince', 'c_cpberar']),
    ('1 Nov 1956', 'The States Reorganisation Act detaches the Marathi-speaking Nagpur and Berar (Amravati) divisions — Buldhana, Akola, Amravati, Yeotmal, Wardha, Nagpur, Bhandara and Chanda — from Madhya Pradesh and adds them to Bombay State, while the Hindi-speaking Jubbulpore, Narmada and Chhattisgarh divisions, together with Madhya Bharat, Vindhya Pradesh and Bhopal, form the reorganised Madhya Pradesh. The old internal divisional line becomes an interstate border.', ['m2', 'c_vidarbha']),
    ('1 May 1960', 'The Bombay Reorganisation Act splits Bombay State into Maharashtra and Gujarat; the Nagpur and Berar districts, as Vidarbha, join Maharashtra, fixing the boundary as it runs today.', ['m4', 'c_vidarbha']),
)

ref('c_chhattisgarhdiv', 'Chhattisgarh Division', 'Wikipedia: a division of the Central Provinces from 1861/62, comprising Raipur, Bilaspur and Sambalpur districts; its princely states passed to the Eastern States Agency in 1933.', 'https://en.wikipedia.org/wiki/Chhattisgarh_Division')
ref('c_esa', 'Eastern States Agency', 'Wikipedia: created 1 April 1933 from the Chhattisgarh States Agency and Orissa States Agency; its 14 Chhattisgarh states (Bastar, Kanker, Raigarh, Sarangarh, Kawardha, Nandgaon, Khairagarh, Surguja, Jashpur, Korea, Udaipur, Chang Bhakar, Sakti and Chhuikhadan) acceded to India in 1947.', 'https://en.wikipedia.org/wiki/Eastern_States_Agency')
ref('c_whitepaper_cg', 'White Paper on Indian States (1950): Orissa and Chhattisgarh States', 'Wikisource: administration of the 39 Orissa and Chhattisgarh states passed to the Orissa and Central Provinces governments on 1 January 1948.', 'https://en.wikisource.org/wiki/White_Paper_on_Indian_States_(1950)/Part_5/Provincially-merged_States/Orissa_and_Chhattisgarh_States')
ref('c_mpreorg2000', 'Madhya Pradesh Reorganisation Act, 2000', 'Wikipedia: enacted 25 August 2000, creating Chhattisgarh state.', 'https://en.wikipedia.org/wiki/Madhya_Pradesh_Reorganisation_Act,_2000')

timeline('Chhattisgarh|Madhya Pradesh',
    ('1853–61', 'Nagpur Province, including Chhattisgarh, is annexed by the British in 1853 and folded into the new Central Provinces in 1861 alongside the Hindi-speaking Saugor and Nerbudda Territories to its north-west.', ['c_nagpurprov', 'c_cp1861']),
    ('1862', 'Chhattisgarh is organised as a division of the Central Provinces, with Raipur as headquarters and Bilaspur and Sambalpur as its other districts; its boundary with the Jubbulpore and Nerbudda divisions is the ancestor of today’s Chhattisgarh–Madhya Pradesh line.', ['c_chhattisgarhdiv']),
    ('1 Apr 1933', 'The Chhattisgarh Feudatory States — Bastar, Kanker, Raigarh, Sarangarh, Kawardha, Nandgaon, Khairagarh, Surguja, Jashpur, Korea, Udaipur, Chang Bhakar, Sakti and Chhuikhadan — are grouped under the new Eastern States Agency, separate from the directly administered Chhattisgarh division but adjoining it.', ['c_esa']),
    ('1 Jan 1948', 'After merger talks led by Sardar Patel and V. P. Menon with the Chhattisgarh rulers at Nagpur on 15 December 1947, the Chhattisgarh Feudatory States, including Bastar and Surguja, merge into the Central Provinces and Berar, enlarging its directly administered territory to roughly its present extent in this sector.', ['c_esa', 'c_whitepaper_cg']),
    ('1 Nov 1956', 'The States Reorganisation Act combines the Hindi-speaking Central Provinces and Berar (minus Marathi Vidarbha) with Madhya Bharat, Vindhya Pradesh and Bhopal into Madhya Pradesh; the old Chhattisgarh divisional line, now enlarged with the former feudatory states, continues as an internal divisional boundary inside the single state.', ['m2']),
    ('25 Aug 2000 / 1 Nov 2000', 'The Madhya Pradesh Reorganisation Act, 2000 carves Chhattisgarh out of sixteen districts — Bastar, Dantewada, Kanker, Jashpur, Raigarh, Korba, Bilaspur, Janjgir-Champa, Rajnandgaon, Kawardha, Durg, Raipur, Mahasamund, Dhamtari, Surguja and Koria — turning the old Chhattisgarh-division/Eastern-States-Agency line into the Chhattisgarh–Madhya Pradesh state border.', ['m29', 'c_mpreorg2000']),
)

ref('c_bastarstate', 'Bastar State', 'Wikipedia: bounded on the west by Chanda District (Central Provinces and Berar), on the north by Kanker State; came under the Central Provinces in 1861, acceded to India 1 January 1948, joined Madhya Pradesh in 1956 and Chhattisgarh in 2000.', 'https://en.wikipedia.org/wiki/Bastar_State')
ref('c_chanda', 'Chandrapur district', 'Wikipedia: as Chanda district it formed part of the Nagpur Division of the Central Provinces and Berar (with Nagpur, Bhandara, Wardha and Balaghat); renamed Chandrapur in 1964.', 'https://familypedia.fandom.com/wiki/Chandrapur_district')

timeline('Chhattisgarh|Maharashtra',
    ('1751–1853', 'Chanda (the future Chandrapur) is ruled by the Gond kings of Chanda, then the Bhonsle Rajas of Nagpur, before Nagpur Province is annexed by the British in 1853.', ['c_chanda', 'c_nagpurprov']),
    ('1861', 'The Central Provinces are formed; Chanda becomes a directly administered district of the Marathi-speaking Nagpur Division, while Bastar becomes a tributary feudatory state of the same province, its western boundary running along Chanda district.', ['c_cp1861', 'c_bastarstate', 'c_chanda']),
    ('1 Jan 1948', 'Bastar, along with the other Chhattisgarh Feudatory States, merges into the Central Provinces and Berar; the Chanda–Bastar line remains an internal boundary within one province.', ['c_bastarstate', 'c_whitepaper_cg']),
    ('1 Nov 1956', 'The States Reorganisation Act moves the Marathi-speaking Nagpur Division, including Chanda, to Bombay State, while Bastar stays with the Hindi-speaking Madhya Pradesh: the Chanda–Bastar/Kanker line becomes an interstate border for the first time.', ['m2', 'c_chanda', 'c_bastarstate']),
    ('1 May 1960', 'The Bombay Reorganisation Act makes Chanda district part of Maharashtra (it is renamed Chandrapur in 1964).', ['m4', 'c_chanda']),
    ('1 Nov 2000', 'The Madhya Pradesh Reorganisation Act, 2000 carves Chhattisgarh out of Madhya Pradesh, including Bastar and Kanker (as Rajnandgaon, Kanker, Bastar, Dantewada districts); the old Chanda–Bastar/Kanker line becomes the Chhattisgarh–Maharashtra border.', ['m29', 'c_mpreorg2000']),
)

ref('c_mysambalpur', 'History of Sambalpur', 'mysambalpur.in: Sambalpur and adjoining Oriya-speaking tracts amalgamated with the Orissa Division of Bengal Presidency in 1905, into Bihar and Orissa Province in 1912, and into the separate Orissa Province in 1936; the Oriya-speaking Phuljhar and Chandarpur zamindaris stayed with the Central Provinces (now Raigarh district, Chhattisgarh).', 'https://www.mysambalpur.in/history/')

timeline('Chhattisgarh|Odisha',
    ('1861', 'Sambalpur and its Oriya-speaking tracts, together with the Phuljhar and Chandarpur zamindaris and the Chhattisgarh division proper, are part of the newly formed Central Provinces.', ['c_cp1861', 'c_mysambalpur']),
    ('1905', 'Sambalpur and most of the adjoining Oriya-speaking tracts are transferred from the Central Provinces to the Orissa Division of Bengal Presidency, but the Oriya-speaking Phuljhar and Chandarpur zamindaris remain with the Central Provinces (today Raigarh district, Chhattisgarh), planting a language mismatch along the line reminiscent of the Berar case.', ['c_mysambalpur']),
    ('22 Mar 1912', 'Bengal’s Orissa Division becomes part of the new Bihar and Orissa Province.', ['biharorissa', 'c_mysambalpur']),
    ('1 Apr 1936', 'Orissa becomes a separate province; its Oriya-speaking princely states (the Garjat states, including Patna, Kalahandi, Sonepur and Bamra) are placed under its authority or the Eastern States Agency, while the Chhattisgarh Feudatory States such as Raigarh and Sarangarh stay grouped on the Central Provinces side of the same agency.', ['m24', 'c_esa']),
    ('1 Jan 1948', 'The Chhattisgarh Feudatory States merge into the Central Provinces and Berar while the neighbouring Orissa princely states merge into Orissa, both effective around the same date, fixing the Eastern States Agency line as the interprovincial boundary.', ['c_whitepaper_cg', 'c_esa']),
    ('1 Nov 1956', 'The States Reorganisation Act reconstitutes Madhya Pradesh from the Central Provinces and Berar (minus Vidarbha) plus Madhya Bharat, Vindhya Pradesh and Bhopal; the former CP–Orissa line becomes the Madhya Pradesh–Orissa border unchanged.', ['m2']),
    ('1 Nov 2000', 'The Madhya Pradesh Reorganisation Act, 2000 carves Chhattisgarh out of Madhya Pradesh, including Raigarh, Sarangarh-Bilaigarh, Jashpur and the Bastar districts; the old Central Provinces–Orissa line becomes the Chhattisgarh–Odisha border.', ['m29', 'c_mpreorg2000']),
)

ref('c_hyderabadannex', 'Indian annexation of Hyderabad', 'Wikipedia: Operation Polo, 13–17 September 1948; Hyderabad State (comprising present-day Telangana, Marathwada and Hyderabad-Karnataka) was annexed to India.', 'https://en.wikipedia.org/wiki/Indian_annexation_of_Hyderabad')
ref('c_adilabad', 'Adilabad district', 'Wikipedia: bounded on the east by Chanda District of the Central Provinces; became part of Andhra Pradesh in 1956 and of Telangana in 2014.', 'https://en.wikipedia.org/wiki/Adilabad_district')

timeline('Chhattisgarh|Telangana',
    ('18th c.', 'The Nizam’s Hyderabad State holds the Adilabad tract, its north-eastern frontier facing the Gond kingdom of Chanda and, later, the Bhonsle Rajas of Nagpur.', ['c_adilabad', 'c_chanda']),
    ('1853–61', 'Nagpur Province, including Chanda, is annexed by the British and folded into the new Central Provinces in 1861; the CP’s south-eastern edge, Chanda district and tributary Bastar State, now faces Hyderabad State along the Godavari River and Adilabad district.', ['c_nagpurprov', 'c_cp1861', 'c_bastarstate']),
    ('13–17 Sep 1948', 'The Government of India annexes Hyderabad State in Operation Polo.', ['c_hyderabadannex']),
    ('1 Nov 1956', 'The States Reorganisation Act merges Hyderabad’s Telangana districts, including Adilabad, into Andhra Pradesh, while the Central Provinces and Berar (minus Vidarbha), with Madhya Bharat, Vindhya Pradesh and Bhopal, form Madhya Pradesh; the old Central Provinces–Hyderabad line along the Godavari becomes the Madhya Pradesh–Andhra Pradesh border.', ['m2', 'c_adilabad']),
    ('1 Nov 2000', 'The Madhya Pradesh Reorganisation Act, 2000 creates Chhattisgarh, including Bastar; its southern boundary with Adilabad becomes the Chhattisgarh–Andhra Pradesh border.', ['m29', 'c_mpreorg2000']),
    ('2 Jun 2014', 'The Andhra Pradesh Reorganisation Act, 2014 creates Telangana from Andhra Pradesh’s northern and western districts, including Adilabad; the Bastar–Adilabad stretch becomes the Chhattisgarh–Telangana border.', ['m10', 'c_adilabad']),
)

ref('c_chotanagpur', 'Chota Nagpur Division', 'Wikipedia: created 1854 under Act XX, comprising Hazaribagh, Ranchi, Palamau, Manbhum and Singhbhum, with the Chota Nagpur (Tributary) States under the Commissioner’s political authority; part of Bihar and Orissa Province from 1912.', 'https://en.wikipedia.org/wiki/Chota_Nagpur_Division')
ref('c_surguja1905', 'History of Surguja district', 'Commissioner, Surguja Division (Chhattisgarh): in 1905 the Hindi-speaking feudatory states of Chang Bhakar, Korea, Surguja, Udaipur and Jashpur were transferred from Bengal to the Central Provinces, while Oriya-speaking states went to the Orissa Tributary States; the group joined the Eastern States Agency in 1936.', 'https://division-surguja.cg.gov.in/history/')

timeline('Chhattisgarh|Jharkhand',
    ('19th c.', 'Surguja, Jashpur, Korea, Udaipur and Chang Bhakar are administered as Chota Nagpur Tributary/Feudatory States under the Commissioner of Bengal’s Chota Nagpur Division, alongside Palamau district (formed 1894) to their north-east.', ['c_chotanagpur', 'c_surguja1905']),
    ('1905', 'With the partition of Bengal, these Hindi-speaking feudatory states are transferred from Bengal to the Central Provinces, while Oriya-speaking Tributary States go the other way to Orissa; Palamau stays behind in Bengal’s Chota Nagpur Division, separating the two administratively for the first time.', ['c_surguja1905']),
    ('22 Mar 1912', 'The Chota Nagpur Division, with Palamau, becomes part of the new Bihar and Orissa Province.', ['biharorissa', 'c_chotanagpur']),
    ('1936', 'Surguja, Jashpur, Korea, Udaipur and Chang Bhakar are grouped into the Eastern States Agency alongside the Chhattisgarh Feudatory States, while Bihar becomes a separate province with Palamau still in its Chota Nagpur Division, fixing the Bengal/Bihar–Central Provinces line close to today’s course.', ['c_surguja1905', 'c_esa', 'biharorissa']),
    ('1 Jan 1948', 'Surguja, Jashpur, Korea, Udaipur and Chang Bhakar merge into the Central Provinces and Berar.', ['c_esa', 'c_whitepaper_cg']),
    ('1 Nov 1956', 'The States Reorganisation Act folds the Central Provinces and Berar (minus Vidarbha), with Madhya Bharat, Vindhya Pradesh and Bhopal, into Madhya Pradesh; the old Central Provinces–Bihar line becomes the Madhya Pradesh–Bihar border.', ['m2']),
    ('1 Nov 2000 / 15 Nov 2000', 'The Madhya Pradesh Reorganisation Act, 2000 creates Chhattisgarh (including Surguja and Jashpur) and the Bihar Reorganisation Act, 2000 creates Jharkhand (including Palamau) from their respective Chota Nagpur-era territories; the old Bengal/Bihar–Central Provinces line becomes the Chhattisgarh–Jharkhand border.', ['m29', 'm9', 'c_mpreorg2000']),
)

ref('c_vizagagency', 'Vizagapatam Hill Tracts Agency', 'Wikipedia: created by Act XXIV of 1839 after the Ghumusar Rebellion of 1835, on the Russell Report of 18 November 1834; administered 14 zamindari estates in the Madras Presidency’s hill tracts adjoining Bastar State.', 'https://en.wikipedia.org/wiki/Vizagapatam_Hill_Tracts_Agency')
ref('c_vizag_rivers', 'Vizagapatam (Imperial Gazetteer extract)', 'Wikisource: the Saveri (Sabari) river forms the frontier between Jeypore and Bastar for many miles, and meets the Sileru near Motu before both flow into the Godavari.', 'https://en.wikisource.org/wiki/Vizagapatam/Chapter_1')
ref('c_andhrastate', 'Andhra State', 'Wikipedia: formed 1 October 1953 from the Telugu-speaking districts of Madras State, including Visakhapatnam (Vizagapatam).', 'https://en.wikipedia.org/wiki/Andhra_State')

timeline('Andhra Pradesh|Chhattisgarh',
    ('1834–39', 'The Vizagapatam Hill Tracts Agency is created in the Madras Presidency after the Ghumusar Rebellion; its interior boundary with the tributary state of Bastar runs along the Saveri (Sabari) and Sileru rivers towards their confluence with the Godavari.', ['c_vizagagency', 'c_vizag_rivers']),
    ('1861', 'Bastar becomes a tributary feudatory state of the new Central Provinces, so the Vizagapatam Agency–Bastar river line becomes, in effect, the Madras Presidency–Central Provinces boundary.', ['c_bastarstate', 'c_cp1861']),
    ('1 Apr 1936', 'Parts of Vizagapatam district and its hill-tracts agency are transferred to the new Orissa Province, but the stretch facing Bastar stays with Madras.', ['m24', 'c_vizagagency']),
    ('1 Oct 1953', 'Andhra State is carved out of Madras State’s Telugu-speaking districts, including Visakhapatnam, inheriting the Bastar frontier.', ['c_andhrastate']),
    ('1 Nov 1956', 'The States Reorganisation Act merges Andhra State with Hyderabad State’s Telugu (Telangana) districts to form Andhra Pradesh, while the Central Provinces and Berar (minus Vidarbha), with Madhya Bharat, Vindhya Pradesh and Bhopal, form Madhya Pradesh; the old Vizagapatam Agency–Bastar line becomes the Andhra Pradesh–Madhya Pradesh border.', ['m2', 'c_andhrastate']),
    ('1 Nov 2000', 'The Madhya Pradesh Reorganisation Act, 2000 creates Chhattisgarh, including Bastar; the line becomes the Andhra Pradesh–Chhattisgarh border.', ['m29', 'c_mpreorg2000']),
    ('2 Jun 2014', 'Telangana splits from Andhra Pradesh, taking most of the former Hyderabad-Telugu frontier with Bastar and leaving Andhra Pradesh with no border against Chhattisgarh.', ['m10']),
    ('2014', 'The Andhra Pradesh Reorganisation (Amendment) Act, 2014 transfers seven Khammam (Telangana) mandals — Kunavaram, VR Puram, Chintur, Kukunoor and Velerupadu wholly, Bhadrachalam and Burgumpadu partly — to Andhra Pradesh for the Polavaram project, giving Andhra Pradesh a short new stretch of frontier with Chhattisgarh’s Sukma district.', ['m11']),
)

timeline('Madhya Pradesh|Rajasthan',
    ('1854', 'The Central India Agency is created; Gwalior, its largest state, is placed under it. To the west, across what becomes this border, lie Kotah, Jhalawar and Tonk of the separate Rajputana Agency, the line running partly along the Chambal.', ['c_ciagency', 'c_gwaliorstate']),
    ('1817–1949', 'Tonk State, created for Amir Khan in 1817, holds six scattered districts: three under the Rajputana Agency (Tonk, Aligarh, Nimbahera) and three under the Central India Agency (Chhabra, Pirawa and Sironj), planting an enclave that straddles the future state line.', ['c_tonkstate']),
    ('28 May 1948', 'Gwalior, Indore and the other Central India states merge into Madhya Bharat; the Rajputana states form the unions that become Rajasthan. The old Central India Agency/Rajputana Agency line becomes the Madhya Bharat–Rajasthan boundary.', ['c_madhyabharat']),
    ('7 Apr 1949', 'Tonk State accedes to India and is absorbed into Rajasthan. Its detached Central India pargana of Sironj, though east of Madhya Bharat, is administered as part of Rajasthan’s Kota district, an enclave across the new state line.', ['c_tonkstate', 'c_vidisha']),
    ('1 Nov 1956', 'The States Reorganisation Act merges Madhya Bharat, Vindhya Pradesh and Bhopal into Madhya Pradesh. In the same reorganisation Sironj is transferred from Rajasthan’s Kota district to Madhya Pradesh’s Vidisha district, and Sunel-Tappa, an outlying part of Madhya Bharat’s Mandsaur district beyond Jhalawar, goes the other way to Rajasthan, straightening the line into today’s border.', ['m2', 'c_vidisha', 'c_sunel']),
)
