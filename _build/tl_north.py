# North: Uttar Pradesh, Uttarakhand, Bihar and the Nepal / central China borders.
# Executed inside timelines.py (ref() and timeline() are in scope).

ref('sugauli', 'Treaty of Sugauli, 1815–16', 'Wikipedia.', 'https://en.wikipedia.org/wiki/Treaty_of_Sugauli')
ref('nepal1860', 'Nepal–Britain Treaty of 1860', 'Wikipedia: return of the lowlands between the Kali and the Rapti.', 'https://en.wikipedia.org/wiki/Nepal%E2%80%93Britain_Treaty_of_1860')
ref('nayamuluk', 'Naya Muluk', 'Wikipedia: Terai restored to Nepal on 11 December 1816 and in 1860.', 'https://en.wikipedia.org/wiki/Naya_Muluk')
ref('kalapani', 'Kalapani territory', 'Wikipedia.', 'https://en.wikipedia.org/wiki/Kalapani_territory')
ref('susta', 'Susta territory', 'Wikipedia: the Gandak’s change of course.', 'https://en.wikipedia.org/wiki/Susta_territory')
ref('stripmaps', '“Strip maps covering 98 pc of Indo-Nepal boundary jointly finalised by two countries: Govt”', 'Business Standard (PTI), 26 June 2019.', 'https://www.business-standard.com/article/pti-stories/strip-maps-covering-98-pc-of-indo-nepal-boundary-jointly-finalised-by-two-countries-govt-119062601295_1.html')
ref('tehri', 'Tehri Garhwal district', 'Wikipedia: division of Garhwal in 1815, merger with Uttar Pradesh in 1949.', 'https://en.wikipedia.org/wiki/Tehri_Garhwal_district')
ref('ukhistory', 'History of Uttarakhand', 'Wikipedia.', 'https://en.wikipedia.org/wiki/History_of_Uttarakhand')
ref('barahoti', 'Barahoti', 'Wikipedia.', 'https://en.wikipedia.org/wiki/Barahoti')
ref('usnagar', 'Udham Singh Nagar district', 'Wikipedia: carved out of Nainital district in 1995.', 'https://en.wikipedia.org/wiki/Udham_Singh_Nagar_district')
ref('bihup1968', 'Bihar and Uttar Pradesh (Alteration of Boundaries) Act, 1968', 'Indian Kanoon: statement of objects, the Trivedi award and transferred villages.', 'https://indiankanoon.org/doc/538826/')
ref('faizabad1775', 'Treaty of Faizabad, 1775', 'Britannica: Benares ceded to the East India Company.', 'https://www.britannica.com/event/Treaty-of-Faizabad')
ref('biharorissa', 'Bihar and Orissa Province', 'Wikipedia: separated from Bengal on 22 March 1912, divided on 1 April 1936.', 'https://en.wikipedia.org/wiki/Bihar_and_Orissa_Province')
ref('companyrule1772', 'Company rule in India', 'Wikipedia: the 1765 Diwani grant after Buxar, and the 1772 shift under Warren Hastings to the Company collecting revenue directly, with a Board of Revenue at Calcutta and Patna.', 'https://en.wikipedia.org/wiki/Company_rule_in_India')
ref('biharsubah1575', 'Bihar Subah', 'Wikipedia: formed in 1575 with its seat at Patna, bordered by the subas of Illahabad and Awadh to the west and Bengal Subah to the east.', 'https://en.wikipedia.org/wiki/Bihar_Subah')
ref('karmanasa', 'Karmanasa River', 'Wikipedia: rises in the Kaimur Range and forms part of today’s Uttar Pradesh–Bihar border (Sonbhadra, Chandauli, Varanasi and Ghazipur on the UP side; Kaimur and Buxar on the Bihar side) before joining the Ganga near Chausa, site of the 1539 battle between Sher Shah and Humayun.', 'https://en.wikipedia.org/wiki/Karmanasa_River')

timeline('Nepal|Uttarakhand',
    ('1791–1815', 'The Gorkhas rule Kumaon (Almora taken 1791) and Garhwal (by 1804).', ['ukhistory']),
    ('1815–16', 'The Treaty of Sugauli (signed 2 December 1815, ratified 4 March 1816): Nepal renounces all lands west of the Kali, which becomes its western boundary; Kumaon passes to the British.', ['sugauli', 'kalapani']),
    ('c. 1865', 'The British treat the watershed, not the river, as the line near the Kali’s source, placing Kalapani in Kumaon.', ['kalapani']),
    ('1954', 'The India–China trade agreement lists Lipulekh as a pass for traders and pilgrims.', ['kalapani', 'sino1954']),
    ('1962', 'After the Sino-Indian War India closes Lipulekh; it reopens for border trade in 1991.', ['kalapani']),
    ('1981–2007', 'A joint technical committee maps the India–Nepal boundary; strip maps cover about 98% of it, all but Kalapani and Susta.', ['susta', 'stripmaps']),
    ('9 Nov 2000', 'Uttarakhand is carved out of Uttar Pradesh; the Kali frontier becomes Uttarakhand’s.', ['m8', 'ukhistory']),
    ('2020', 'Nepal publishes a map claiming Kalapani, Lipulekh and Limpiyadhura (20 May) and writes it into its constitution (13 June).', ['kalapani']),
)

timeline('Nepal|Uttar Pradesh',
    ('1815–16', 'By the Treaty of Sugauli Nepal cedes the Terai lowlands to the East India Company.', ['sugauli']),
    ('11 Dec 1816', 'Part of the Terai is given back to Nepal.', ['nayamuluk']),
    ('1 Nov 1860', 'For Nepal’s help in 1857, Britain returns “the whole of the lowlands between the Rivers Kali and Raptee” and those between the Rapti and Gorakhpur district (the Naya Muluk). Their southern edge is essentially today’s UP–Nepal line.', ['nepal1860', 'nayamuluk']),
    ('1981–2007', 'A joint technical committee maps the boundary; strip maps cover about 98% of the India–Nepal border.', ['susta', 'stripmaps']),
)

timeline('Bihar|Nepal',
    ('1765', 'After the Treaty of Allahabad the East India Company controls Bihar as part of Bengal.', ['biharorissa']),
    ('1815–16', 'The Treaty of Sugauli: Nepal cedes the Terai; in this sector the Gandak serves as the boundary.', ['sugauli', 'susta']),
    ('11 Dec 1816', 'The Terai from the Rapti to the Gandak and from the Gandak to the Koshi is restored to Nepal, leaving the Champaran–Purnea frontier close to its present line.', ['nayamuluk']),
    ('22 Mar 1912', 'Bihar and Orissa province is separated from Bengal; the Nepal frontier becomes Bihar’s.', ['biharorissa']),
    ('20th c.', 'The Gandak shifts east, leaving Susta, once on Nepal’s bank, on the Indian side; the area remains disputed.', ['susta']),
    ('1981–2007', 'A joint technical committee maps about 98% of the India–Nepal boundary, excluding Susta and Kalapani.', ['susta', 'stripmaps']),
)

timeline('Uttar Pradesh|Uttarakhand',
    ('1815–16', 'After the Anglo-Gorkha War, Kumaon and eastern Garhwal go to the British and western Garhwal becomes the princely state of Tehri.', ['tehri', 'ukhistory']),
    ('British period', 'Kumaon and Garhwal are administered as divisions of the North-Western Provinces, later the United Provinces.', ['ukhistory']),
    ('Aug 1949', 'Tehri is merged into Uttar Pradesh as a district.', ['tehri']),
    ('Oct 1995', 'Udham Singh Nagar district is carved out of Nainital.', ['usnagar']),
    ('9 Nov 2000', 'The Uttar Pradesh Reorganisation Act, 2000 creates Uttarakhand from the Kumaon and Garhwal divisions plus Haridwar district; their outer district lines become the state boundary.', ['m8', 'ukhistory']),
)

timeline('Himachal Pradesh|Uttarakhand',
    ('1803–15', 'The Gorkhas occupy Garhwal, Dehradun and the Shimla hills.', ['tehri']),
    ('1815–16', 'The British keep Dehradun and eastern Garhwal and restore western Garhwal as Tehri; Jaunsar-Bawar, formerly part of Sirmur, is kept and added to Chakrata tahsil in 1829.', ['tehri', 'ukhistory']),
    ('15 Apr 1948', 'The hill states on the western side, such as Sirmaur, become Himachal Pradesh.', ['hphistory']),
    ('1949–60', 'Tehri merges into Uttar Pradesh (August 1949); Uttarkashi becomes a separate district in 1960.', ['tehri']),
    ('9 Nov 2000', 'Uttarakhand is formed; the line becomes the Himachal–Uttarakhand boundary.', ['m8']),
)

timeline('China|Uttarakhand',
    ('1815–16', 'Kumaon and eastern Garhwal, with their passes into Tibet, pass to the British; western Garhwal becomes Tehri state.', ['sugauli', 'tehri']),
    ('29 Apr 1954', 'The India–China trade agreement lists the Mana, Niti and Lipulekh passes, among others.', ['sino1954']),
    ('Jun 1954', 'The first Chinese incursion into Indian territory takes place at Barahoti; China sets up a camp there in 1955.', ['barahoti']),
    ('1962', 'After the Sino-Indian War, Lipulekh is closed; it reopens for trade in 1991.', ['kalapani']),
    ('7 Sep 1993', 'India and China agree to respect the Line of Actual Control; Barahoti remains disputed.', ['bpta1993', 'barahoti']),
    ('9 Nov 2000', 'Uttarakhand is formed.', ['m8']),
)

timeline('Bihar|Uttar Pradesh',
    ('1575', 'Akbar’s provincial reorganisation creates Bihar Subah, seated at Patna, with the subas of Illahabad and Awadh on its western side — the ancestor of this border. In its southern stretch the line already runs the Karmanasa, which still separates Uttar Pradesh’s Sonbhadra, Chandauli, Varanasi and Ghazipur districts from Bihar’s Kaimur and Buxar today; further north and east, the shifting channels of the Ganga and Ghaghra (Saryu) mark it instead, which is why those rivers keep unsettling the line in later centuries.', ['biharsubah1575', 'karmanasa']),
    ('1765', 'After the Company’s victory at Buxar (1764), the Treaty of Allahabad has Mughal emperor Shah Alam II grant it the Diwani — the right to collect revenue — over Bengal, Bihar and Odisha; day-to-day administration stays with the existing Mughal machinery, so the Company is not yet Bihar’s direct ruler.', ['companyrule1772']),
    ('1772', 'Governor Warren Hastings ends that arrangement: the Company takes over revenue collection itself, setting up a Board of Revenue at Calcutta and Patna and moving the Mughal revenue records there from Murshidabad. The Company becomes Bihar’s direct ruler for the first time.', ['companyrule1772']),
    ('1775', 'The Treaty of Faizabad cedes Benares to the Company, bringing British rule up to Bihar’s western edge.', ['faizabad1775']),
    ('22 Mar 1912', 'Bihar and Orissa province is separated from Bengal; the old Bengal–United Provinces line becomes Bihar’s western boundary.', ['biharorissa']),
    ('1 Apr 1936', 'Bihar becomes a province on its own.', ['biharorissa']),
    ('1961–64', 'The shifting Ganga and Ghaghra keep moving villages across the line; the chief ministers refer it to arbitration, and C. M. Trivedi reports on 28 August 1964 recommending a fixed boundary.', ['bihup1968']),
    ('1968', 'The Bihar and Uttar Pradesh (Alteration of Boundaries) Act fixes the boundary on the 1963–64 deep stream: about 45 sq mi move from UP to Bihar and about 64 sq mi from Bihar to UP (Saran and Shahabad vs Ballia).', ['bihup1968']),
)
