# South 2: Karnataka with Kerala, Maharashtra and Tamil Nadu; Kerala with Tamil Nadu and
# Puducherry; Puducherry–Tamil Nadu.
# Executed inside timelines.py (ref() and timeline() are in scope).

ref('s2_kodagu', 'Kodagu district', 'Wikipedia: the Haleri dynasty, 1834 annexation, Coorg province, 1956 merger into Mysore State.', 'https://en.wikipedia.org/wiki/Kodagu_district')
ref('s2_malabar', 'Malabar District', 'Wikipedia: 1792 cession by Tipu Sultan, Bombay then Madras Presidency, the 1956 States Reorganisation Act.', 'https://en.wikipedia.org/wiki/Malabar_District')
ref('s2_kanara', 'South Canara', 'Wikipedia: the 1799 annexation of Kanara, the 1859–62 split of North and South Kanara, and the 1956 partition between Mysore and Kerala.', 'https://en.wikipedia.org/wiki/South_Canara')
ref('s2_kasaragod', 'Kasaragod district', 'Wikipedia: Kumbla and Nileshwaram chieftaincies, South Canara, 19th-century agitation to join Malabar, and transfer to Kerala in 1956.', 'https://en.wikipedia.org/wiki/Kasaragod_district')
ref('s2_karnataka', 'Karnataka', 'Wikipedia: renaming of Mysore State to Karnataka, 1 November 1973.', 'https://en.wikipedia.org/wiki/Karnataka')
ref('s2_belgaum', 'Belagavi district', 'Wikipedia: Peshwa- and Mysore-era rule, 1818 British acquisition, 1836 district formation, and the 1956 transfer to Mysore State.', 'https://en.wikipedia.org/wiki/Belagavi_district')
ref('s2_belgaumdispute', 'Belagavi border dispute', 'Wikipedia: the 1956 reorganisation, the Maharashtra Ekikaran Samiti, the Mahajan Commission (1966–67) and the Supreme Court suit.', 'https://en.wikipedia.org/wiki/Belagavi_border_dispute')
ref('s2_seringapatam1792', 'Treaty of Seringapatam (1792)', 'Wikipedia: Tipu Sultan cedes the Baramahal, Dindigul and part of Malabar to the East India Company; Kodagu is made a separate protected state.', 'https://en.wikipedia.org/wiki/Treaty_of_Seringapatam')
ref('s2_mysore1799', 'Kingdom of Mysore', 'Wikipedia: the 1799 partition after Tipu Sultan’s death and the restoration of Krishnaraja III of the Wadiyar dynasty as ruler of a reduced princely state.', 'https://en.wikipedia.org/wiki/Kingdom_of_Mysore')
ref('s2_coimbatore', 'History, Coimbatore District', 'Government of Tamil Nadu: 1799 cession of the Kongu region, the 1804 district under a single Collector, and the 1956 transfer of Kollegal taluk to Mysore State.', 'https://coimbatore.nic.in/history/')
ref('s2_nilgiris', 'History, The Nilgiris District', 'Government of Tamil Nadu: separation from Coimbatore district in August 1868 and full district status in February 1882.', 'https://nilgiris.nic.in/about-district/history/')
ref('s2_travancore', 'Travancore', 'Wikipedia: extent against the Madurai and Tirunelveli districts of Madras Presidency, and the Tamil character of the Padmanabhapuram (Kanyakumari) division.', 'https://en.wikipedia.org/wiki/Travancore')
ref('s2_poonjar', 'Poonjar dynasty', 'Wikipedia: the Pandya-descended chiefdom of the Devikulam–Peermade hill tract and its gradual absorption by Travancore.', 'https://en.wikipedia.org/wiki/Poonjar_dynasty')
ref('s2_travancorecochin', 'Travancore-Cochin', 'Wikipedia: formation on 1 July 1949, and the 1956 States Reorganisation Act transfer of Kanyakumari and Shencottah to Madras while Devikulam and Peermade stayed in Kerala.', 'https://en.wikipedia.org/wiki/Travancore-Cochin')
ref('s2_devikulam', '“Historically and demographically, Peermedu and Devikulam taluks belong to TN”', 'The Weekend Leader: a Tamil Nadu-side account of the Poonjar kingdom, the resettlement of Malayalam-speaking families and the demand revived around 2012.', 'https://www.theweekendleader.com/Causes/912/idukki-for-tn.html')
ref('s2_mahe', 'Mahé, India', 'Wikipedia: the 1724 fort built under an accord with the Vazhunnavar of Vatakara, British capture and the 1763 and 1785 restorations, and the 13 June 1954 liberation.', 'https://en.wikipedia.org/wiki/Mah%C3%A9,_India')
ref('s2_frenchindia', 'French India', 'Wikipedia: the five enclaves, the Treaty of Paris 1763, their stabilisation at about 510 sq km by 1950, and the 1954–63 transfer to India.', 'https://en.wikipedia.org/wiki/French_India')
ref('s2_puducherryhist', 'History of Puducherry', 'Wikipedia: the 1674 settlement, the piecemeal acquisition of Karaikal (1738) and outlying villages, and the 1954, 1956 and 1962 transfer dates.', 'https://en.wikipedia.org/wiki/History_of_Puducherry')

timeline('Karnataka|Kerala',
    ('c. 1600–1834', 'Kodagu (Coorg), ruled by the Haleri dynasty, borders the Malabar country of the Zamorin of Calicut and the Kolathunadu chiefs; this dynastic frontier is the ancestor of today’s Kodagu–Wayanad stretch of the line.', ['s2_kodagu']),
    ('1792', 'The Treaty of Seringapatam, ending the Third Anglo-Mysore War, forces Tipu Sultan to cede Malabar, including Wayanad, to the East India Company; it is placed under Bombay Presidency at first, then transferred to Madras Presidency in 1800.', ['s2_malabar']),
    ('1799', 'After Tipu Sultan’s defeat and death in the Fourth Anglo-Mysore War, the Company annexes the Kanara coast and joins North and South Kanara into one district of Madras Presidency.', ['s2_kanara']),
    ('1834', 'The Company annexes Kodagu, deposing Chikka Virarajendra, and administers it as the separate province of Coorg, fixing its border against British Malabar to the west.', ['s2_kodagu']),
    ('1859–62', 'Kanara district is split: North Kanara is transferred to Bombay Presidency by 1862, while South Canara — including the Malayalam-majority Kasaragod taluk — stays under Madras, despite 19th-century agitation to merge Kasaragod into neighbouring Malabar.', ['s2_kanara', 's2_kasaragod']),
    ('1947–50', 'After independence, Coorg becomes a separate Part C state, while Malabar and South Canara (with Kasaragod) remain districts of Madras State; the three still meet near Kodagu’s south-western corner.', ['s2_kodagu']),
    ('1 Nov 1956', 'The States Reorganisation Act merges Coorg into the enlarged Mysore State and merges Malabar into the new state of Kerala. It also detaches Kasaragod taluk from South Canara and gives it to Kerala, joining Kannur district, while the rest of South Canara becomes Mysore’s Dakshina Kannada district — fixing the Karnataka–Kerala line, from Kasaragod to Wayanad and Kodagu, as it runs today.', ['m2', 's2_kasaragod']),
    ('1 Nov 1973', 'Mysore State is renamed Karnataka; the boundary itself is unchanged.', ['s2_karnataka']),
)

timeline('Karnataka|Tamil Nadu',
    ('18 Mar 1792', 'The Treaty of Seringapatam ends the Third Anglo-Mysore War: Tipu Sultan cedes about half his kingdom to the allies, including the Baramahal and Dindigul districts, to the East India Company, and Kodagu (Coorg) becomes a separate, British-protected state — the first carve-out of territory now on the Tamil Nadu side of the line.', ['s2_seringapatam1792']),
    ('1799', 'After Tipu Sultan’s death in the Fourth Anglo-Mysore War, Mysore is partitioned: the reduced kingdom is restored to the Wadiyar dynasty as a princely state, while the Company keeps Coimbatore (the Kongu country), Baramahal, Dindigul and Malabar as Madras Presidency territory bordering it.', ['s2_mysore1799', 's2_coimbatore']),
    ('1804', 'Coimbatore’s two revenue divisions are merged under a single Collector, fixing it as a Madras Presidency district along the line ceded in 1792 and 1799.', ['s2_coimbatore']),
    ('Aug 1868', 'The Nilgiris, until then part of Coimbatore district, become a separate Madras Presidency district (full district status follows in 1882), adding the Gudalur–Wynaad sector to the Mysore frontier.', ['s2_nilgiris']),
    ('1799–1956', 'For over 150 years the Mysore–Madras line runs along this cession boundary — the princely state of Mysore against the Coimbatore, Salem and Nilgiris districts of Madras Presidency and then Madras State.', ['s2_mysore1799']),
    ('1 Nov 1956', 'The States Reorganisation Act transfers the whole of Kollegal taluk from Madras State’s Coimbatore district to the enlarged Mysore State on linguistic grounds — the one substantial shift of the old cession line, and the change that produced today’s Karnataka–Tamil Nadu border.', ['m2', 's2_coimbatore']),
    ('1 Nov 1973', 'Mysore State is renamed Karnataka; the boundary itself is unchanged.', ['s2_karnataka']),
)

timeline('Kerala|Tamil Nadu',
    ('1792–1868', 'In the north, the line follows the old edge of Malabar district — ceded by Tipu Sultan in 1792 — against Coimbatore and, after August 1868, the separate Nilgiris district of Madras Presidency: the origin of today’s Palakkad Gap and Gudalur–Wayanad sector.', ['s2_malabar', 's2_nilgiris']),
    ('19th c.', 'In the south, Travancore’s eastern border runs against the Madurai and Tirunelveli districts of Madras Presidency; its own southernmost division, Padmanabhapuram (roughly today’s Kanyakumari district), is already Tamil-majority.', ['s2_travancore']),
    ('18th–19th c.', 'The Poonjar chiefdom, descended from the Pandyas of Madurai and ruling the Devikulam–Peermade hill tract further north, is progressively absorbed by Travancore, which leases and then annexes its remaining territory.', ['s2_poonjar']),
    ('1 Jul 1949', 'Travancore and Cochin merge to form Travancore-Cochin, a Part B state; its eastern border with Madras Presidency, soon Madras State, still runs along the old Travancore line.', ['s2_travancorecochin']),
    ('1 Nov 1956', 'The States Reorganisation Act cuts the Tamil-majority Agastheeswaram, Thovala, Kalkulam and Vilavancode taluks and the Shencottah taluk out of Travancore-Cochin for Madras State, where they form Kanyakumari district — but keeps the Tamil-majority Devikulam and Peermade taluks in the new state of Kerala, citing a resettlement of thousands of Malayalam-speaking families there as evidence of the government’s commitment to the area. The rest of Travancore-Cochin merges with Malabar to form Kerala the same day.', ['m2', 's2_travancorecochin']),
    ('2012–', 'The transfer of Devikulam and Peermade is periodically revived as a Tamil Nadu political demand, especially amid disputes over the Mullaperiyar dam; Kerala regards the 1956 line, and the taluks’ place within it, as settled.', ['s2_devikulam']),
)

timeline('Kerala|Puducherry',
    ('1721–24', 'The French East India Company agrees terms with the Vazhunnavar (Kolathiri chief) of Vatakara and builds a fort at Mahé, on the Malabar coast.', ['s2_mahe']),
    ('1761–63', 'The British capture Mahé in 1761; the Treaty of Paris of 1763 restores it to France as an unfortified trading post, an enclave surrounded by British Malabar.', ['s2_mahe', 's2_frenchindia']),
    ('1779–85', 'Renewed Anglo-French war costs France Mahé again; it is restored for the last time in 1785, after which its limits against Malabar stay essentially fixed for over a century and a half.', ['s2_mahe']),
    ('13 Jun 1954', 'Local pro-merger activists take over the administration of Mahé; France recognises the de facto transfer to India along with Pondichéry, Karaikal and Yanam on 1 November 1954.', ['s2_mahe', 's2_frenchindia']),
    ('16 Aug 1962', 'France ratifies the Treaty of Cession, completing the de jure transfer of the four French territories to India.', ['m20', 's2_frenchindia']),
    ('1 Jul 1963', 'Mahé becomes one of the four regions of the new Union Territory of Puducherry, its old comptoir boundary now the line between Puducherry and Kerala’s Kannur and Kozhikode districts.', ['m20', 's2_puducherryhist']),
)

timeline('Puducherry|Tamil Nadu',
    ('1673–74', 'The French East India Company sets up a trading post at Pondichéry.', ['s2_puducherryhist']),
    ('1738–39', 'France acquires Karaikal from the Thanjavur Maratha ruler, a separate coastal enclave inside the Tamil country.', ['s2_puducherryhist']),
    ('1761–63', 'The British capture Pondichéry and the other French posts in 1761; the Treaty of Paris of 1763 restores them but confines France to unfortified trading posts. France responds by buying up neighbouring villages piecemeal — Arikamedu, Kakayanthope, Villianur and Bahur among them — producing the irregular, scattered enclave pattern that survives today.', ['s2_frenchindia', 's2_puducherryhist']),
    ('1779–85', 'A further round of Anglo-French war costs France its Indian posts again; they are restored for the last time in 1785.', ['s2_frenchindia']),
    ('1816', 'After the Napoleonic Wars, France recovers Pondichéry, Karaikal and its other Indian settlements for good; the five together total about 510 sq km, their boundaries against British and then Madras territory essentially unchanged thereafter.', ['s2_frenchindia']),
    ('1 Nov 1954', 'French and Indian representatives agree the de facto transfer of Pondichéry, Karaikal, Mahé and Yanam to Indian administration.', ['s2_frenchindia', 's2_puducherryhist']),
    ('28 May 1956', 'France and India sign the Treaty of Cession.', ['s2_puducherryhist']),
    ('16 Aug 1962 / 1 Jul 1963', 'France ratifies the treaty on 16 August 1962, completing the de jure transfer; Pondicherry, Karaikal, Mahé and Yanam are organised as the Union Territory of Puducherry on 1 July 1963, fixing today’s border — Puducherry and Karaikal’s old French village limits, plus their outlying exclaves, embedded within Tamil Nadu.', ['m20', 's2_puducherryhist']),
)

timeline('Karnataka|Maharashtra',
    ('1818', 'The East India Company takes Belgaum from the Peshwa — Hyder Ali of Mysore had briefly overrun it in 1776 — and joins it to Dharwar district; Belgaum becomes a separate district in 1836, one of the Bombay Presidency’s Kannada-speaking “Karnatak” districts.', ['s2_belgaum']),
    ('1836–1862', 'The Bombay Presidency’s Kannada-speaking districts take shape: Belgaum (1836), Dharwad and Bijapur, and North Kanara (added from Madras Presidency by 1862); together they border the Marathi-speaking Deccan districts of Satara, Kolhapur and Sangli.', ['s2_belgaum', 's2_kanara']),
    ('1948', 'The Maharashtra Ekikaran Samiti forms at Belgaum, campaigning to keep the mixed-language Bombay Presidency districts of Belgaum, Bijapur, Dharwad and North Kanara united with a future Marathi-speaking state rather than a Kannada one.', ['s2_belgaumdispute']),
    ('1 Nov 1956', 'The States Reorganisation Act moves Belgaum, Bijapur, Dharwad and North Kanara from Bombay State to the new, enlarged Mysore State on linguistic grounds; Maharashtra’s claim to Belgaum and other Marathi-speaking pockets within them begins here.', ['m2', 's2_belgaumdispute']),
    ('1 May 1960', 'The Bombay Reorganisation Act splits the remaining bilingual Bombay State into Gujarat and Maharashtra. Because the Karnatak districts had already left Bombay State in 1956, Maharashtra inherits the boundary dispute rather than the territory.', ['m4']),
    ('1957–66', 'Maharashtra petitions the Union government; a four-member committee set up in 1960 deadlocks, and at Maharashtra’s insistence the Government of India constitutes the Mahajan Commission, under former Chief Justice Meher Chand Mahajan, on 25 October 1966.', ['s2_belgaumdispute']),
    ('Aug 1967', 'The Mahajan Commission, after reviewing over 2,240 memoranda and interviewing more than 7,500 people, rejects Maharashtra’s claim to Belgaum city and recommends about 264 villages (including Nippani and Khanapur) to Maharashtra and about 247 (including Jatt and Akkalkot) to Karnataka. Maharashtra rejects the report as “biased and self-contradictory”; it is tabled in Parliament in 1970 and never implemented, leaving the 1956 line in place.', ['s2_belgaumdispute']),
    ('c. 2005', 'Maharashtra files an original suit in the Supreme Court over Belgaum and other disputed villages — sources differ on whether this was 2004 or 2006 — while Karnataka maintains that the Mahajan report is final; the case remains pending and the 1956 line continues to apply on the ground.', ['s2_belgaumdispute']),
)
