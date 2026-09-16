# North-east, part 2: Myanmar, Bangladesh, Bhutan and China frontiers of the
# north-eastern states. Executed inside timelines.py (ref() and timeline() are in scope).

# -----------------------------------------------------------------------------
# Myanmar borders: Arunachal Pradesh, Nagaland, Manipur, Mizoram
# -----------------------------------------------------------------------------
ref('nx_yandabo', 'Treaty of Yandabo', 'Wikipedia: 24 February 1826; Burma cedes Assam and Manipur and agrees to stop interfering on the frontier.', 'https://en.wikipedia.org/wiki/Treaty_of_Yandabo')
ref('nx_kabaw', 'Kabaw Valley', 'Wikipedia: transfer to Burmese administration on 9 January 1834 and the Pemberton line drawn to its west; compensation payments to Manipur discontinued in 1953.', 'https://en.wikipedia.org/wiki/Kabaw_Valley')
ref('nx_kabawcomp', 'Agreement Regarding Compensation for the Kubo (Kabaw) Valley (1834)', 'Wikipedia: signed 25 January 1834 at Langthabal between Major F. J. Grant/Captain R. B. Pemberton and Raja Gambhir Singh of Manipur; monthly allowance of 500 Sicca rupees.', 'https://en.wikipedia.org/wiki/Agreement_Regarding_Compensation_for_the_Kubo_(Kabaw)_Valley_(1834)')
ref('nx_pemberton', 'Robert Boileau Pemberton', 'Wikipedia: the 1834 Manipur–Kabaw Valley line and the 1894 Manipur–Chin Hills boundary drawn close to it.', 'https://en.wikipedia.org/wiki/Robert_Boileau_Pemberton')
ref('nx_johnstone', '“Contested history”', 'ForumIAS Blog: the 1834 Pemberton line, its 1881 revision by Colonel James Johnstone (Chassad tract), the 1896 Pemberton–Johnstone–Maxwell line and its 1967 ratification.', 'https://forumias.com/blog/contested-history/')
ref('nx_burma1937', 'Burma separated from British India, 1 April 1937', 'The Irrawaddy: the Government of Burma Act 1935 took effect on 1 April 1937, making Burma a separate Crown colony under Premier Ba Maw.', 'https://www.irrawaddy.com/specials/on-this-day/burma-separated-british-india-82-years-ago-today.html')
ref('nx_1967brookings', 'India and Myanmar: the boundary agreement of 1967', 'Brookings (Sambandh blog): the Rangoon agreement of 10 March 1967 formalised a colonial-era administrative line; Mizo and Naga insurgencies pushed India to settle it; mapping errors cost India ground near Moreh.', 'https://www.brookings.edu/articles/sambandh-blog-india-and-myanmar-the-role-of-domestic-calculations-in-the-boundary-agreement-of-1967/')
ref('nx_lushaihills', 'British rule in the Lushai Hills', 'Wikipedia: the January 1892 Chin-Lushai Conference, the Viceroy’s ruling of 2 August 1892 keeping the Chin Hills under Burma, the 1898 unification of the Lushai Hills district and the 1901 boundary commission.', 'https://en.wikipedia.org/wiki/British_rule_in_the_Lushai_Hills')
ref('nx_arunstate', 'Arunachal Pradesh Day', 'Wikipedia: statehood on 20 February 1987 as India’s 24th state.', 'https://en.wikipedia.org/wiki/Arunachal_Pradesh_Day')
ref('nx_nefa', 'Arunachal Pradesh: the evolution from NEFA to statehood', 'BA Notes: NEFA constituted 1954; renamed the Union Territory of Arunachal Pradesh in 1972; full statehood in 1987.', 'https://banotes.org/democracy-development-northeast/arunachal-pradesh-evolution-nefa-statehood/')
ref('nx_mizostate', 'Mizoram (union territory)', 'Wikipedia: created a Union Territory on 21 January 1972 under the North-Eastern Areas (Reorganisation) Act, 1971; statehood 20 February 1987.', 'https://en.wikipedia.org/wiki/Mizoram_(union_territory)')
ref('nx_nagahills', 'Naga Hills District, British India', 'Wikipedia: district created 1866, with the Lotha (1875), Ao (1889), Sümi (1904) and Konyak (1910) tracts annexed to it.', 'https://en.wikipedia.org/wiki/Naga_Hills_District,_British_India')

timeline('Arunachal Pradesh|Myanmar',
    ('1826', 'The Treaty of Yandabo ends the First Anglo-Burmese War: Burma cedes Assam and agrees to stop interfering on the frontier, bringing the tracts north of the Patkai within the British sphere even though no precise line is drawn there.', ['nx_yandabo']),
    ('1826–1937', 'Burma itself remains a province of British India, so the Patkai range functions only as an internal administrative watershed between Assam’s frontier tracts and Burma, not an international boundary.', ['nx_burma1937']),
    ('1 Apr 1937', 'The Government of Burma Act 1935 separates Burma from British India; the Patkai watershed, already the practical edge of British administration on this stretch, becomes an international frontier.', ['nx_burma1937']),
    ('1954', 'The North-East Frontier Agency (NEFA) is constituted to administer the tracts on the Indian side of the Patkai, including what are now Arunachal’s Changlang and Anjaw districts.', ['nx_nefa']),
    ('10 Mar 1967', 'India and Burma sign a boundary agreement at Rangoon delimiting and demarcating their entire common frontier, from the China trijunction to the Bangladesh trijunction, largely following the traditional Patkai watershed in this sector.', ['nx_1967brookings']),
    ('21 Jan 1972', 'NEFA is renamed and made the Union Territory of Arunachal Pradesh; the demarcated Patkai line becomes its external frontier with Burma.', ['nx_nefa', 'nx_arunstate']),
    ('20 Feb 1987', 'Arunachal Pradesh becomes India’s 24th state under the State of Arunachal Pradesh Act, 1986; the Patkai line remains its boundary with Myanmar.', ['nx_arunstate']),
)

timeline('Myanmar|Nagaland',
    ('1826', 'The Treaty of Yandabo ends the First Anglo-Burmese War and brings the Naga-inhabited hills within the British sphere, though the frontier beyond the Patkai watershed is left undefined.', ['nx_yandabo']),
    ('1866–1910', 'British Assam creates the Naga Hills district in 1866 and extends it east through the annexation of Lotha (1875), Ao (1889), Sümi (1904) and Konyak (1910) tracts, its unadministered far side approaching the Patkai.', ['nx_nagahills']),
    ('1 Apr 1937', 'Burma is separated from British India under the Government of Burma Act 1935; the Patkai watershed, the practical limit of British administration here, becomes an international frontier.', ['nx_burma1937']),
    ('10 Mar 1967', 'India and Burma sign the Rangoon boundary agreement, delimiting and demarcating the whole common frontier, including the Patkai stretch bordering Naga country.', ['nx_1967brookings']),
    ('1 Dec 1963', 'Nagaland becomes India’s 16th state under the State of Nagaland Act, 1962; the demarcated Patkai line becomes its boundary with Myanmar.', ['m5']),
)

timeline('Manipur|Myanmar',
    ('1826', 'The Treaty of Yandabo ends the First Anglo-Burmese War: Burma renounces its claims to Manipur, whose eastern limit towards the Kabaw Valley is left undefined.', ['nx_yandabo']),
    ('9 Jan 1834', 'Manipur, which had held the Kabaw Valley since the war, is required to hand it back to Burmese administration.', ['nx_kabaw']),
    ('25 Jan 1834', 'At Langthabal, Grant and Pemberton draw the Pemberton line along the base of the Yomadong (Muring) hills west of the Kabaw Valley; Manipur is compensated with a monthly allowance of 500 Sicca rupees, to lapse if the valley is ever restored to it.', ['nx_pemberton', 'nx_kabawcomp']),
    ('1881', 'A commission under Colonel James Johnstone shifts the line to keep the disputed Chassad tract inside Manipur, producing the Pemberton–Johnstone line; Burma is invited but does not attend.', ['nx_johnstone']),
    ('1896', 'A further revision, adding surveyor Maxwell’s name, produces the Pemberton–Johnstone–Maxwell line, which becomes the standard reference boundary.', ['nx_johnstone']),
    ('21 Sep 1949', 'The Manipur Merger Agreement brings the princely state into the Indian Union with its existing external limits intact.', ['m34']),
    ('3 Mar 1953', 'Nehru and Burmese premier U Nu agree to end the compensation payments for the Kabaw Valley, discontinuing a subsidy that had run for more than a century.', ['nx_kabaw']),
    ('10 Mar 1967', 'India and Burma sign the Rangoon boundary agreement ratifying the Pemberton–Johnstone–Maxwell line; errors in the accompanying maps left some Manipuri-claimed ground, including territory near Moreh, on the Myanmar side.', ['nx_johnstone', 'nx_1967brookings']),
)

timeline('Mizoram|Myanmar',
    ('1826', 'The Treaty of Yandabo brings Cachar within the British sphere; the Lushai Hills to its south remain unadministered and only loosely bounded from the Chin Hills to their east.', ['nx_yandabo']),
    ('25–29 Jan 1892', 'At a Chin-Lushai Conference in Calcutta, officials debate uniting the Chin and Lushai Hills under one administration; the Chief Commissioner of Burma objects.', ['nx_lushaihills']),
    ('2 Aug 1892', 'The Viceroy rules that the Chin Hills stay under Burma, separate from the Lushai Hills under Assam — the origin of today’s Mizoram–Myanmar line.', ['nx_lushaihills']),
    ('1 Apr 1898', 'The North and South Lushai Hills are merged into a single Lushai Hills district under Assam, with Aizawl as headquarters.', ['nx_lushaihills']),
    ('1901', 'A boundary commission demarcates the Chin–Lushai frontier along the Tuipui and Tuisai streams into the Tuimang and Bopuilui, up to the source of the Tyao river.', ['nx_lushaihills']),
    ('1 Apr 1937', 'Burma is separated from British India under the Government of Burma Act 1935; the 1892/1901 Chin–Lushai administrative line becomes an international frontier.', ['nx_burma1937', 'nx_lushaihills']),
    ('10 Mar 1967', 'India and Burma sign the Rangoon boundary agreement, delimiting and demarcating the whole common frontier, including this stretch.', ['nx_1967brookings']),
    ('21 Jan 1972', 'The Lushai Hills, by then renamed Mizo Hills, become the Union Territory of Mizoram under the North-Eastern Areas (Reorganisation) Act, 1971; the demarcated Chin Hills line becomes its boundary with Myanmar.', ['m7', 'nx_mizostate']),
    ('20 Feb 1987', 'Mizoram becomes India’s 23rd state under the State of Mizoram Act, 1986.', ['nx_mizostate']),
)

# -----------------------------------------------------------------------------
# Bangladesh borders: Assam, Meghalaya, Tripura, Mizoram
# -----------------------------------------------------------------------------
ref('nx_sylhet', 'Undivided Sylhet district', 'Wikipedia: transfer from Bengal to Assam in September 1874, the 6–7 July 1947 referendum (423,660 for East Bengal to 123,155 for Assam) and the retention of Karimganj sub-division by India.', 'https://en.wikipedia.org/wiki/Undivided_Sylhet_district')
ref('nx_radcliffe', 'Radcliffe Line', 'Wikipedia: the Bengal Boundary Commission’s award of 17 August 1947, its Muslim/non-Muslim contiguous-majority principle, and the award of the 97%-non-Muslim Chittagong Hill Tracts to Pakistan; Karimganj later became an Assam district in 1983.', 'https://en.wikipedia.org/wiki/Radcliffe_Line')
ref('nx_cht', 'Brief History of the Chittagong Hill Tracts', 'UPDFCHT: British annexation in 1860, the Chittagong Hill Tracts Regulation of 1900, and the 1947 award of the CHT to Pakistan despite its non-Muslim majority.', 'https://updfcht.com/?page_id=45')
ref('nx_lba', 'India–Bangladesh enclaves', 'Wikipedia: the Indira–Mujib Land Boundary Agreement signed 16 May 1974, the September 2011 Additional Protocol, the Constitution (100th Amendment) Act’s passage in May 2015, and the enclave exchange at midnight on 31 July/1 August 2015 (India gained 51 enclaves, 7,110 acres; Bangladesh gained 111, 17,160 acres).', 'https://en.wikipedia.org/wiki/India%E2%80%93Bangladesh_enclaves')
ref('nx_tripurastate', 'Tripura (princely state)', 'Wikipedia: the Chakla Roshnabad zamindari in the Comilla/Noakhali/Sylhet plains, British protectorate status from 1809, recognition of the Rajas as sovereigns in 1838, and inclusion in Eastern Bengal and Assam as ‘Hill Tippera’ from 1905.', 'https://en.wikipedia.org/wiki/Tripura_(princely_state)')
ref('nx_tripuramerger', 'Tripura Merger Agreement', 'Wikipedia: signed 9 September 1949 by Regent Maharani Kanchan Prava Devi, effective 15 October 1949.', 'https://en.wikipedia.org/wiki/Tripura_Merger_Agreement')
ref('nx_khasijaintia', 'Khasi and Jaintia Hills', 'Wikipedia: organised as a district of Assam from 1912 to 1947, immediately north of the Sylhet plains.', 'https://en.wikipedia.org/wiki/Khasi_and_Jaintia_Hills')
ref('nx_meghstate', 'Meghalaya’s journey from “state within a state” to full statehood', 'PolSci Institute: the autonomous state of Meghalaya formed 2 April 1970 under the Assam Reorganisation (Meghalaya) Act, 1969, and full statehood on 21 January 1972 under the North-Eastern Areas (Reorganisation) Act, 1971.', 'https://polsci.institute/india-political-process/meghalaya-journey-to-full-statehood/')

timeline('Assam|Bangladesh',
    ('Sep 1874', 'Sylhet district, previously part of Bengal and valued for its tea revenue, is transferred to the new Assam Chief-Commissionership, setting Assam’s southern frontier against the Bengal districts to its south.', ['nx_sylhet']),
    ('6–7 Jul 1947', 'A referendum asks Sylhet’s voters whether the district should join the future East Bengal; 423,660 vote to join against 123,155 to remain with Assam.', ['nx_sylhet']),
    ('17 Aug 1947', 'The Radcliffe Bengal Boundary Commission’s award sends most of Sylhet to East Bengal but, after local lobbying, keeps the Karimganj sub-division — three and a half thanas — with India as part of Assam, giving the Barak Valley its present shape.', ['m13', 'nx_sylhet']),
    ('1983', 'Karimganj becomes a separate Assam district; its western edge along the former Sylhet line is the international border.', ['nx_radcliffe']),
    ('16 May 1974', 'The Indira–Mujib Land Boundary Agreement addresses enclaves and adverse possessions along the whole India–Bangladesh border, including Assam’s stretch.', ['nx_lba']),
    ('31 Jul–1 Aug 2015', 'The Constitution (100th Amendment) Act, 2015 gives the 1974 agreement and its 2011 protocol legal effect; outstanding adverse possessions are settled and the boundary, including Assam’s section, is finally demarcated.', ['m28', 'nx_lba']),
)

timeline('Bangladesh|Meghalaya',
    ('1874', 'Sylhet is transferred from Bengal to the new Assam province; the Khasi and Jaintia Hills, already under British administration, sit immediately north of the Sylhet and Mymensingh plains.', ['nx_sylhet', 'nx_khasijaintia']),
    ('1912', 'The Khasi and Jaintia Hills and the Garo Hills are organised as districts of Assam; their southern limits against Sylhet and Mymensingh become the line later inherited by Meghalaya.', ['nx_khasijaintia']),
    ('17 Aug 1947', 'The Radcliffe Bengal Boundary Commission’s award places Sylhet and Mymensingh in East Bengal, fixing the hills–plains district line as an international border.', ['m13']),
    ('2 Apr 1970', 'Meghalaya is created as an autonomous state within Assam, combining the Khasi &amp; Jaintia Hills and Garo Hills districts and their Bangladesh-facing frontier.', ['nx_meghstate']),
    ('21 Jan 1972', 'Meghalaya becomes a full state under the North-Eastern Areas (Reorganisation) Act, 1971.', ['m7', 'nx_meghstate']),
    ('2015', 'The Constitution (100th Amendment) Act, 2015 gives effect to the 1974 Land Boundary Agreement and its 2011 protocol, settling adverse possessions and completing demarcation along Meghalaya’s border.', ['m28', 'nx_lba']),
)

timeline('Bangladesh|Tripura',
    ('1809', 'Tripura becomes a British protectorate; its plains estate of Chakla Roshnabad, in the Comilla, Noakhali and Sylhet region, is held as a zamindari under the Nawab of Bengal even as the hill kingdom stays internally independent.', ['nx_tripurastate']),
    ('1838', 'The British recognise the Manikya Rajas of Tripura as sovereigns, formalising the princely state’s status alongside the surrounding British Bengal districts of Comilla, Noakhali, Sylhet and Chittagong.', ['nx_tripurastate']),
    ('1905', 'Tripura is placed alongside the short-lived province of Eastern Bengal and Assam, styled ‘Hill Tippera’; its boundary with the Bengal districts is unchanged.', ['nx_tripurastate']),
    ('17 Aug 1947', 'The Radcliffe Bengal Boundary Commission’s award places Comilla, Noakhali, Sylhet and the Chittagong Hill Tracts in East Bengal (later East Pakistan), while princely Tripura, hemmed in on three sides, stays outside Pakistan.', ['m13', 'nx_cht']),
    ('9 Sep 1949', 'The Tripura Merger Agreement, signed by Regent Maharani Kanchan Prava Devi, brings the state into the Indian Union with effect from 15 October 1949, its existing external limits against East Pakistan intact.', ['nx_tripuramerger']),
    ('21 Jan 1972', 'Tripura becomes a full state under the North-Eastern Areas (Reorganisation) Act, 1971.', ['m7']),
    ('2015', 'The Constitution (100th Amendment) Act, 2015 gives effect to the 1974 Land Boundary Agreement and its 2011 protocol, settling adverse possessions along Tripura’s border with Bangladesh.', ['m28', 'nx_lba']),
)

timeline('Bangladesh|Mizoram',
    ('1860', 'The British occupy the Chittagong Hill Tracts, administered as an extension of Chittagong district; the Lushai country to its north and east remains outside British control.', ['nx_cht']),
    ('2 Aug 1892', 'The Viceroy’s decision keeping the Chin Hills under Burma, separate from the Lushai Hills, leaves the Lushai Hills’ southern neighbour as the Chittagong Hill Tracts, already under a separate Bengal administration.', ['nx_lushaihills']),
    ('1900', 'The Chittagong Hill Tracts Regulation gives the CHT a distinct, restricted-settlement administration under Bengal, sharpening its separation from the Lushai Hills district administered from Assam.', ['nx_cht']),
    ('17 Aug 1947', 'At independence the Chittagong Hill Tracts, despite a large non-Muslim majority, are awarded to Pakistan by the Radcliffe Bengal Boundary Commission; the inherited Lushai Hills–CHT administrative line becomes an international frontier.', ['m13', 'nx_cht']),
    ('21 Jan 1972', 'The Lushai Hills, renamed Mizo Hills, become the Union Territory of Mizoram under the North-Eastern Areas (Reorganisation) Act, 1971.', ['m7', 'nx_mizostate']),
    ('2015', 'The Constitution (100th Amendment) Act, 2015 gives effect to the 1974 Land Boundary Agreement and its 2011 protocol, settling adverse possessions and completing demarcation along Mizoram’s border with Bangladesh.', ['m28', 'nx_lba']),
    ('20 Feb 1987', 'Mizoram becomes India’s 23rd state; the CHT line stays as its border with Bangladesh.', ['nx_mizostate']),
)

# -----------------------------------------------------------------------------
# Bhutan borders: Arunachal Pradesh, Assam
# -----------------------------------------------------------------------------
ref('nx_assamduars', 'The Duar War, 1864–1865', 'onwar.com: Britain’s 1841 annexation of the Assam Duars for an annual Rs 10,000 compensation, the failed 1863 Eden mission, the war declared 12 November 1864, and the Treaty of Sinchula’s cession of the Bengal and Assam Duars plus the Kalimpong tract for a subsidy rising to Rs 50,000.', 'https://onwar.com/data/britbhutan1865.html')
ref('nx_punakha', 'Treaty of Punakha', 'Wikipedia: signed 8 January 1910, effective 10 January; it amended the 1865 Treaty of Sinchula’s financial and diplomatic articles, doubling the subsidy and giving Britain charge of Bhutan’s external relations, without altering the boundary.', 'https://en.wikipedia.org/wiki/Treaty_of_Punakha')
ref('nx_1949treaty', 'Treaty of Perpetual Peace and Friendship between India and Bhutan (1949)', 'Advocatetanmoy: signed 8 August 1949 at Darjeeling; India to return about 32 square miles of the Dewangiri tract within a year and pay an annual subsidy of five lakh rupees.', 'https://advocatetanmoy.com/peace-treaty-india-bhutan/')
ref('nx_bhutanindiaborder', 'Bhutan–India border', 'Wikipedia: the 1774 peace treaty, the 1841–42 Duars annexation, the 1865/1910/1949 treaties, boundary delimitation surveys of 1973–1984 with minor disagreements on the Arunachal Pradesh stretch, and a final demarcation treaty in 2006.', 'https://en.wikipedia.org/wiki/Bhutan%E2%80%93India_border')

timeline('Arunachal Pradesh|Bhutan',
    ('1774', 'A peace treaty between the East India Company, acting after intervening in a Cooch Behar succession dispute, and Bhutan gives the first British recognition of a Bhutanese frontier.', ['nx_bhutanindiaborder']),
    ('1841', 'Britain annexes the Assam Duars from Bhutan, paying an annual compensation of Rs 10,000; the British-administered plains now run up against the Bhutan hills along the future Arunachal sector.', ['nx_assamduars']),
    ('1864–65', 'The Duar War: Britain withholds the Duars compensation after a failed 1863 mission under Ashley Eden, then declares war on 12 November 1864; Bhutan loses about a fifth of its territory.', ['nx_assamduars']),
    ('11 Nov 1865', 'The Treaty of Sinchula: Bhutan cedes the Bengal and Assam Duars and the Kalimpong hill tract in perpetuity for an annual subsidy rising to Rs 50,000 — the cession line becomes the origin of the modern Bhutan–India frontier, including its eastern, Arunachal-facing stretch.', ['nx_assamduars']),
    ('8 Jan 1910', 'The Treaty of Punakha revises the 1865 settlement’s financial and diplomatic terms — doubling the subsidy and putting Bhutan’s foreign relations under British guidance — without moving the boundary.', ['nx_punakha']),
    ('8 Aug 1949', 'The India–Bhutan Treaty of Perpetual Peace and Friendship replaces the 1910 treaty; India agrees to return about 32 square miles of the Dewangiri tract to Bhutan within a year, adjusting the frontier’s eastern end.', ['nx_1949treaty']),
    ('1973–1984', 'Joint surveys delimit the boundary in detail; minor disagreements remain over short stretches next to Arunachal Pradesh.', ['nx_bhutanindiaborder']),
    ('2006', 'India and Bhutan sign a final border demarcation treaty settling the remaining stretches; the line stands as Arunachal Pradesh’s boundary with Bhutan.', ['nx_bhutanindiaborder']),
)

timeline('Assam|Bhutan',
    ('1774', 'A peace treaty between the Company and Bhutan, following British intervention in a Cooch Behar succession dispute, gives the first British recognition of Bhutan’s southern frontier.', ['nx_bhutanindiaborder']),
    ('1841', 'Britain annexes the Assam Duars — lowland tracts in Darrang and Kamrup — from Bhutan, paying an annual compensation of Rs 10,000.', ['nx_assamduars']),
    ('1864–65', 'The Duar War: after Britain withholds the Duars compensation and a mission under Ashley Eden fails, war is declared on 12 November 1864; Bhutanese forces briefly retake ground before Britain prevails.', ['nx_assamduars']),
    ('11 Nov 1865', 'The Treaty of Sinchula: Bhutan permanently cedes the Bengal and Assam Duars, about a fifth of its territory, for an annual subsidy rising to Rs 50,000 — the origin of today’s Assam–Bhutan line.', ['nx_assamduars']),
    ('8 Jan 1910', 'The Treaty of Punakha revises the 1865 treaty’s terms, doubling the subsidy and giving Britain charge of Bhutan’s foreign relations, without moving the boundary.', ['nx_punakha']),
    ('8 Aug 1949', 'The India–Bhutan Treaty of Perpetual Peace and Friendship replaces the 1910 treaty and keeps the 1865 cession line as the international boundary along Assam.', ['nx_1949treaty']),
    ('1973–1984', 'Joint surveys formally delimit the boundary; the Assam stretch is settled without major dispute.', ['nx_bhutanindiaborder']),
)

# -----------------------------------------------------------------------------
# China border: Arunachal Pradesh
# -----------------------------------------------------------------------------
ref('nx_simla1914', 'Simla Accord (1914)', 'Wikipedia: negotiated at Simla between Britain’s Henry McMahon and Tibet’s Lonchen Shatra; China’s delegate Ivan Chen initialled the draft on 27 April 1914 but never signed the final convention of 3 July 1914.', 'https://en.wikipedia.org/wiki/Simla_Accord_(1914)')
ref('nx_tawang1951', 'Ralengnao Khathing', 'Wikipedia: Assam Rifles troops under Major Ralengnao “Bob” Khathing took possession of Tawang and raised Indian administration up to the McMahon Line (dated 1951 in most accounts, 1950 in this article).', 'https://en.wikipedia.org/wiki/Ralengnao_Khathing')
ref('nx_mcmahon', 'McMahon Line', 'Wikipedia: the 1914 Simla Convention line, its non-enforcement until the 1950s, the 1962 war (Chinese forces advancing to Walong and near Bomdila before withdrawing to the line), and the present dispute, with China rejecting the line while treating it as part of the Line of Actual Control.', 'https://en.wikipedia.org/wiki/McMahon_Line')
ref('nx_cbm1996', 'Agreement on Military Confidence Building Measures, 1996', 'Wikipedia: signed in New Delhi on 29 November 1996, limiting forces and weapons near the Line of Actual Control and setting up flag-meeting procedures, while noting differing perceptions of the LAC’s alignment in places.', 'https://en.wikipedia.org/wiki/Agreement_on_Military_Confidence_Building_Measures,_1996')

timeline('Arunachal Pradesh|China',
    ('1913–14', 'At the Simla Convention, British India’s Henry McMahon and Tibet’s Lonchen Shatra negotiate a boundary along the crest of the eastern Himalaya — the McMahon Line — while China’s delegate initials the draft in April 1914 but never signs the final convention of 3 July.', ['nx_simla1914']),
    ('1914–1940s', 'Britain does little to enforce the new line on the ground; Tawang continues to be administered through its monastery under Lhasa, and successive Chinese governments never recognise the convention.', ['nx_mcmahon']),
    ('Feb 1951', 'Assam Rifles troops under Major Ralengnao “Bob” Khathing take possession of Tawang and raise Indian administration up to the McMahon Line for the first time.', ['nx_tawang1951']),
    ('1954', 'The North-East Frontier Agency (NEFA) is constituted to administer the whole tract south of the McMahon Line, including Tawang.', ['nx_nefa']),
    ('20 Oct–21 Nov 1962', 'In the Sino-Indian War, Chinese forces cross the McMahon Line, take Tawang and advance about 30 km beyond Walong and close to Bomdila, before declaring a unilateral ceasefire and withdrawing back to the line.', ['nx_mcmahon']),
    ('7 Sep 1993', 'India and China sign the Border Peace and Tranquility Agreement, agreeing to respect the Line of Actual Control pending a boundary settlement.', ['bpta1993']),
    ('29 Nov 1996', 'A further agreement on military confidence-building measures limits forces and weapons near the LAC and sets up flag-meeting procedures, while recording “differing perceptions” of its exact alignment in places.', ['nx_cbm1996']),
    ('1972–1987', 'NEFA becomes the Union Territory and then, on 20 February 1987, the state of Arunachal Pradesh; China rejects the McMahon Line, calls the state “South Tibet” and claims most of it, while India administers up to the line, which functions as the de facto Line of Actual Control in this sector.', ['nx_arunstate', 'nx_mcmahon']),
)
