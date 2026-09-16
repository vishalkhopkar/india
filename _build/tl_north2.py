# North, remainder: Jharkhand, Chhattisgarh, Madhya Pradesh and Rajasthan with Uttar Pradesh.
# Executed inside timelines.py (ref() and timeline() are in scope).

ref('n2_palamu', 'Palamu district', 'Wikipedia: British annexation after a tenant revolt against the Chero raja, part of the Chota Nagpur Division, reconstituted as a separate district in 1892.', 'https://en.wikipedia.org/wiki/Palamu_district')
ref('n2_chotanagpur', 'Chota Nagpur Division', 'Wikipedia: formed 1854 under Act XX from the South West Frontier Agency, comprising Hazaribagh, Ranchi, Palamau, Manbhum and Singhbhum; part of Bihar and Orissa province from 1912 to 1936.', 'https://en.wikipedia.org/wiki/Chota_Nagpur_Division')
ref('n2_sonbhadra', 'Sonbhadra district', 'Wikipedia: established 4 March 1989 from the southern part of Mirzapur district.', 'https://en.wikipedia.org/wiki/Sonbhadra_district')
ref('n2_garhwa', 'Garhwa district', 'Wikipedia: established 1 April 1991 from Palamu district; bordered by the Son River to the north and Sonbhadra district of Uttar Pradesh to the west.', 'https://en.wikipedia.org/wiki/Garhwa_district')
ref('n2_surguja', 'Surguja State', 'Wikipedia: founded 1613, a British protectorate from 1818 after the Third Anglo-Maratha War, placed under the Central India Agency and transferred to the Eastern States Agency in 1905; acceded to India 1 January 1948.', 'https://en.wikipedia.org/wiki/Surguja_State')
ref('n2_esa', 'Eastern States Agency', 'Wikipedia: the Chhattisgarh States group (Surguja, Jashpur, Korea, Udaipur, Changbhakar and others) within the Agency.', 'https://en.wikipedia.org/wiki/Eastern_States_Agency')
ref('n2_whitepaper_chg', 'White Paper on Indian States (1950): Orissa and Chhattisgarh States', 'Wikisource: merger agreements signed from 14 December 1947, administration transferred to the Central Provinces on 1 January 1948.', 'https://en.wikisource.org/wiki/White_Paper_on_Indian_States_(1950)/Part_5/Provincially-merged_States/Orissa_and_Chhattisgarh_States')
ref('n2_balrampur_cg', 'Balrampur district, Chhattisgarh', 'Wikipedia: created 17 January 2012 from Surguja district; borders Uttar Pradesh to the north.', 'https://en.wikipedia.org/wiki/Balrampur_district,_Chhattisgarh')
ref('n2_bundelkhand', 'Bundelkhand Agency', 'Wikipedia: created 1811, headquartered at Banda; placed under the Central India Agency in 1854; bounded by the United Provinces to the north and the Central Provinces to the south; lasted until 1948.', 'https://en.wikipedia.org/wiki/Bundelkhand_Agency')
ref('n2_jhansi', 'Doctrine of lapse', 'Wikipedia/Grokipedia: Jhansi State annexed by the British in 1853 after the death of Raja Gangadhar Rao without a natural heir.', 'https://en.wikipedia.org/wiki/Doctrine_of_lapse')
ref('n2_lalitpur', 'Lalitpur district, India', 'Wikipedia: Chanderi annexed by Gwalior in 1812, acquired by the British in 1844; in 1861 the portion west of the Betwa (including Chanderi) returned to Gwalior and the remainder renamed Lalitpur district; part of Jhansi district 1891–1974, separate again from 1974.', 'https://en.wikipedia.org/wiki/Lalitpur_district,_India')
ref('n2_vindhya', 'Vindhya Pradesh', 'Wikipedia: formed 12 March/4 April 1948 as the Union of Baghelkhand and Bundelkhand States (36 princely states, capital Rewa); on 25 January 1950 eleven small states (Bihat, Banka Paharee, Baoni, Beri, Bijna, Charkhari, Jigni, Samthar, Sarila, Tori-Fatehpur and parts of Kirar Kubja) were transferred to Uttar Pradesh and Madhya Bharat; merged into Madhya Pradesh 1 November 1956.', 'https://en.wikipedia.org/wiki/Vindhya_Pradesh')
ref('n2_bharatpur', 'Bharatpur State', 'Wikipedia: territory once reached Agra and Dholpur; treaty with the British after Ranjit Singh backed Holkar (1805); fortress stormed by British forces 18 January 1826; acceded to India August 1947, joined the Matsya Union 1948 and Rajasthan 1949.', 'https://en.wikipedia.org/wiki/Bharatpur_State')
ref('n2_dholpur', 'Dholpur state', 'Wikipedia: created 1805 when Rana Kirat Singh received Dholpur in exchange for Gohad; a princely state under British suzerainty from 1818; bordered by Agra district of Uttar Pradesh to the north.', 'https://en.wikipedia.org/wiki/Dholpur_state')
ref('n2_karauli', 'Karauli state', 'Wikipedia: subsidiary alliance with the East India Company signed 9 November 1817; acceded to the Dominion of India with Alwar, Bharatpur and Dholpur to form the Matsya Union.', 'https://en.wikipedia.org/wiki/Karauli_state')

timeline('Jharkhand|Uttar Pradesh',
    ('1775', 'The Treaty of Faizabad cedes Benares to the East India Company, including the territory later organised as Mirzapur district.', ['faizabad1775']),
    ('after 1800', 'British troops annex Palamu, on the south bank of the Son, after suppressing a tenant revolt against the Chero raja.', ['n2_palamu']),
    ('1854', 'Palamu becomes one of five districts of the new Chota Nagpur Division, formed under Act XX of 1854 within the Bengal Presidency.', ['n2_chotanagpur']),
    ('1892', 'Palamu is reconstituted as a separate district of the Division, facing Mirzapur district across the Son.', ['n2_palamu']),
    ('22 Mar 1912', 'Bihar and Orissa Province is separated from Bengal: Palamu and the rest of Chota Nagpur join it, while Mirzapur remains in the United Provinces of Agra and Oudh on the far bank.', ['biharorissa']),
    ('1 Apr 1936', 'Bihar becomes a province in its own right.', ['biharorissa']),
    ('4 Mar 1989', 'Sonbhadra district is carved from the southern part of Mirzapur district, becoming the Uttar Pradesh district that fronts Chota Nagpur along the Son.', ['n2_sonbhadra']),
    ('1 Apr 1991', 'Garhwa district is separated from Palamu, becoming the Bihar district that faces Sonbhadra across the river.', ['n2_garhwa']),
    ('15 Nov 2000', 'The Bihar Reorganisation Act, 2000 creates Jharkhand from the southern districts, including Garhwa and Palamu; their stretch of the Son against Sonbhadra becomes the Jharkhand–Uttar Pradesh border.', ['m9']),
)

timeline('Chhattisgarh|Uttar Pradesh',
    ('1775', 'The Treaty of Faizabad cedes Benares to the East India Company, the origin of the later Mirzapur district that fronts the hill country to the south.', ['faizabad1775']),
    ('1818', 'After the Third Anglo-Maratha War, Surguja becomes a British protectorate; its frontier against Mirzapur district becomes the line between British territory and the princely state.', ['n2_surguja']),
    ('1905', 'Surguja is transferred from the Central India Agency to the new Eastern States Agency, as part of its Chhattisgarh States group.', ['n2_esa', 'n2_surguja']),
    ('14 Dec 1947 – 1 Jan 1948', 'Surguja and the other Chhattisgarh States sign merger agreements with the Dominion government; administration passes to the Central Provinces and Berar on 1 January 1948.', ['n2_whitepaper_chg', 'n2_surguja']),
    ('1 Nov 1956', 'The States Reorganisation Act forms the enlarged Madhya Pradesh; Surguja stays in it, so the old Surguja–Mirzapur frontier remains the Madhya Pradesh–Uttar Pradesh boundary.', ['m2']),
    ('4 Mar 1989', 'Sonbhadra district is carved from Mirzapur, becoming the Uttar Pradesh district that fronts Surguja.', ['n2_sonbhadra']),
    ('1 Nov 2000', 'The Madhya Pradesh Reorganisation Act, 2000 creates Chhattisgarh, including Surguja district; the line becomes the Chhattisgarh–Uttar Pradesh border.', ['m29']),
    ('17 Jan 2012', 'Balrampur district is carved from Surguja; it, rather than Surguja itself, now fronts Uttar Pradesh along most of this border.', ['n2_balrampur_cg']),
)

timeline('Madhya Pradesh|Uttar Pradesh',
    ('1811–54', 'The British Bundelkhand Agency, formed 1811 and headquartered at Banda, oversees Orchha, Panna, Datia and other Bundelkhand states south of the United Provinces; it is placed under the wider Central India Agency in 1854.', ['n2_bundelkhand']),
    ('1812', 'Daulat Rao Sindhia of Gwalior annexes Chanderi, the state that later becomes Lalitpur district.', ['n2_lalitpur']),
    ('1844', 'The British acquire the Chanderi territory, administering it as Chanderi district with Lalitpur as headquarters.', ['n2_lalitpur']),
    ('1853', 'Jhansi State lapses to the British under the Doctrine of Lapse after the death of Raja Gangadhar Rao, extending British Bundelkhand territory against the Orchha and Datia states to the south.', ['n2_jhansi']),
    ('1861', 'After the 1857 revolt, the part of Chanderi district west of the Betwa (including Chanderi town) is handed back to Gwalior state; the remainder is renamed Lalitpur district, leaving it almost surrounded by princely territory.', ['n2_lalitpur']),
    ('1891–1974', 'Lalitpur is administered as part of Jhansi district.', ['n2_lalitpur']),
    ('1948', 'The Bundelkhand and Baghelkhand states (Orchha, Panna, Datia, Chhatarpur, Rewa and others) merge into the new Vindhya Pradesh, while Gwalior joins Madhya Bharat; both border the United Provinces.', ['n2_vindhya']),
    ('25 Jan 1950', 'Eleven small former Vindhya Pradesh states near Jhansi, including Charkhari, Samthar, Sarila and Baoni, are transferred to Uttar Pradesh, adding to the jagged shape of the line around Jhansi and Lalitpur.', ['n2_vindhya']),
    ('1 Nov 1956', 'The States Reorganisation Act merges Vindhya Pradesh, Madhya Bharat and Bhopal into Madhya Pradesh, and forms Uttar Pradesh from the United Provinces; the old princely-state edges, and the Chambal and Yamuna for long stretches, become the interstate boundary.', ['m2']),
    ('1974', 'Lalitpur becomes a separate Uttar Pradesh district again, still bounded on three sides by Madhya Pradesh.', ['n2_lalitpur']),
)

timeline('Rajasthan|Uttar Pradesh',
    ('30 Dec 1803', 'The Treaty of Surji-Anjangaon: Scindia cedes Agra and the Delhi–Agra tract to the British, fixing the future United Provinces side of the frontier against Bharatpur, Dholpur and Karauli.', ['surji']),
    ('1805', 'After Bharatpur backs Holkar against the British, its fort is besieged and a new treaty makes it a British-protected state; the same year Rana Kirat Singh receives Dholpur in exchange for Gohad, creating a buffer state fronting British Agra district.', ['n2_bharatpur', 'n2_dholpur']),
    ('9 Nov 1817', 'Karauli signs a subsidiary alliance with the East India Company.', ['n2_karauli']),
    ('1818', 'Dholpur passes under full British suzerainty as a princely state.', ['n2_dholpur']),
    ('18 Jan 1826', 'British forces storm Bharatpur’s fortress after a succession dispute, fixing its status as a British-protected state on the Agra frontier.', ['n2_bharatpur']),
    ('Aug 1947', 'Alwar, Bharatpur, Dholpur and Karauli accede to the Dominion of India.', ['n2_bharatpur', 'n2_karauli']),
    ('18 Mar 1948', 'The four states form the Matsya Union.', ['matsya']),
    ('15 May 1949', 'The Matsya Union merges into Greater Rajasthan; the old Bharatpur–Dholpur–Karauli edge against Agra and Mathura becomes the Rajasthan–Uttar Pradesh state line.', ['matsya', 'whitepaper_raj']),
)
