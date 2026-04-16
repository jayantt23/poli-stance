from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

# Minimal mock registry. Replace/extend this with your researched registry.
MOCK_TARGET_REGISTRY: Dict[str, Dict[str, Any]] = {
    # India
    "Narendra Modi": {
        "aliases": ["Narendra Modi", "Modi", "PM Modi", "Prime Minister Modi"],
        "related": ["BJP"],
        "kind": "person",
        "country": "india",
    },
    "Rahul Gandhi": {
        "aliases": ["Rahul Gandhi", "Rahul"],
        "related": ["Congress"],
        "kind": "person",
        "country": "india",
    },
    "Mamata Banerjee": {
        "aliases": ["Mamata Banerjee", "Mamata", "Didi", "CM Mamata"],
        "related": ["TMC"],
        "kind": "person",
        "country": "india",
    },
    "Amit Shah": {
        "aliases": ["Amit Shah", "Shah", "Home Minister Amit Shah"],
        "related": ["BJP"],
        "kind": "person",
        "country": "india",
    },
    "BJP": {
        "aliases": ["BJP", "Bharatiya Janata Party"],
        "related": ["Narendra Modi", "Amit Shah"],
        "kind": "party",
        "country": "india",
    },
    "Congress": {
        "aliases": ["Congress", "INC", "Indian National Congress"],
        "related": ["Rahul Gandhi", "Mallikarjun Kharge"],
        "kind": "party",
        "country": "india",
    },
    "TMC": {
        "aliases": [
            "TMC",
            "Trinamool",
            "Trinamool Congress",
            "All India Trinamool Congress",
        ],
        "related": ["Mamata Banerjee"],
        "kind": "party",
        "country": "india",
    },
    "AAP": {
        "aliases": ["AAP", "Aam Aadmi Party"],
        "related": ["Arvind Kejriwal"],
        "kind": "party",
        "country": "india",
    },
    "Arvind Kejriwal": {
        "aliases": ["Arvind Kejriwal", "Kejriwal"],
        "related": ["AAP"],
        "kind": "person",
        "country": "india",
    },
    "Mallikarjun Kharge": {
        "aliases": ["Mallikarjun Kharge", "Kharge"],
        "related": ["Congress"],
        "kind": "person",
        "country": "india",
    },
    "Demonetisation": {
        "aliases": [
            "Demonetisation",
            "demonetization",
            "demonetised",
            "demonetized",
            "notebandi",
        ],
        "related": [],
        "kind": "issue",
        "country": "india",
    },
    "Delimitation": {
        "aliases": ["Delimitation", "delimitation"],
        "related": [],
        "kind": "issue",
        "country": "india",
    },
    "Women's Reservation Bill": {
        "aliases": [
            "Women's Reservation Bill",
            "women's reservation bill",
            "women's quota",
            "women quota",
            "33 per cent reservation",
            "33% reservation",
        ],
        "related": [],
        "kind": "issue",
        "country": "india",
    },
    "CAA": {
        "aliases": ["CAA", "Citizenship Amendment Act", "Citizenship (Amendment) Act"],
        "related": [],
        "kind": "issue",
        "country": "india",
    },
    "Farm Laws": {
        "aliases": ["Farm Laws", "farm laws", "three farm laws"],
        "related": [],
        "kind": "issue",
        "country": "india",
    },
    # US
    "Donald Trump": {
        "aliases": ["Donald Trump", "Trump", "President Trump"],
        "related": ["Republican Party"],
        "kind": "person",
        "country": "us",
    },
    "Joe Biden": {
        "aliases": ["Joe Biden", "Biden", "President Biden"],
        "related": ["Democratic Party"],
        "kind": "person",
        "country": "us",
    },
    "Bernie Sanders": {
        "aliases": ["Bernie Sanders", "Bernie", "Sanders"],
        "related": ["Democratic Party"],
        "kind": "person",
        "country": "us",
    },
    "Kamala Harris": {
        "aliases": ["Kamala Harris", "Kamala", "Vice President Harris"],
        "related": ["Democratic Party"],
        "kind": "person",
        "country": "us",
    },
    "Republican Party": {
        "aliases": ["Republican Party", "Republicans", "GOP"],
        "related": ["Donald Trump"],
        "kind": "party",
        "country": "us",
    },
    "Democratic Party": {
        "aliases": ["Democratic Party", "Democrats", "Dems"],
        "related": ["Joe Biden", "Bernie Sanders", "Kamala Harris"],
        "kind": "party",
        "country": "us",
    },
}

TARGET_REGISTRY = {
    # INDIA – PEOPLE
    "Narendra Modi": {
        "aliases": [
            "Narendra Modi",
            "Modi",
            "PM Modi",
            "Prime Minister Modi",
            "Namo",
            "NaMo",
            "Modi ji",
        ],
        "kind": "person",
        "country": "india",
    },
    "Amit Shah": {
        "aliases": ["Amit Shah", "Shah", "Home Minister Shah", "Amit bhai"],
        "kind": "person",
        "country": "india",
    },
    "Rajnath Singh": {
        "aliases": ["Rajnath Singh", "Rajnath", "Defence Minister Singh"],
        "kind": "person",
        "country": "india",
    },
    "Nitin Gadkari": {
        "aliases": ["Nitin Gadkari", "Gadkari"],
        "kind": "person",
        "country": "india",
    },
    "Nirmala Sitharaman": {
        "aliases": [
            "Nirmala Sitharaman",
            "Sitharaman",
            "Finance Minister Sitharaman",
            "FM Sitharaman",
        ],
        "kind": "person",
        "country": "india",
    },
    "S. Jaishankar": {
        "aliases": [
            "S. Jaishankar",
            "Jaishankar",
            "EAM Jaishankar",
            "External Affairs Minister Jaishankar",
            "Subrahmanyam Jaishankar",
        ],
        "kind": "person",
        "country": "india",
    },
    "Yogi Adityanath": {
        "aliases": [
            "Yogi Adityanath",
            "Yogi",
            "CM Yogi",
            "Adityanath",
            "Chief Minister Yogi",
        ],
        "kind": "person",
        "country": "india",
    },
    "Mallikarjun Kharge": {
        "aliases": ["Mallikarjun Kharge", "Kharge", "Congress President Kharge"],
        "kind": "person",
        "country": "india",
    },
    "Rahul Gandhi": {
        "aliases": ["Rahul Gandhi", "Rahul", "RaGa", "Pappu"],
        "kind": "person",
        "country": "india",
    },
    "Sonia Gandhi": {
        "aliases": ["Sonia Gandhi", "Sonia", "UPA Chairperson Sonia"],
        "kind": "person",
        "country": "india",
    },
    "Priyanka Gandhi Vadra": {
        "aliases": [
            "Priyanka Gandhi Vadra",
            "Priyanka Gandhi",
            "Priyanka",
            "Priyanka Vadra",
        ],
        "kind": "person",
        "country": "india",
    },
    "Manmohan Singh": {
        "aliases": [
            "Manmohan Singh",
            "Manmohan",
            "Dr. Manmohan Singh",
            "Former PM Manmohan Singh",
        ],
        "kind": "person",
        "country": "india",
    },
    "Arvind Kejriwal": {
        "aliases": ["Arvind Kejriwal", "Kejriwal", "AK", "Delhi CM Kejriwal"],
        "kind": "person",
        "country": "india",
    },
    "Atishi": {
        "aliases": ["Atishi", "Atishi Marlena", "Atishi Singh"],
        "kind": "person",
        "country": "india",
    },
    "Manish Sisodia": {
        "aliases": ["Manish Sisodia", "Sisodia"],
        "kind": "person",
        "country": "india",
    },
    "Mamata Banerjee": {
        "aliases": [
            "Mamata Banerjee",
            "Mamata",
            "Didi",
            "CM Mamata",
            "Bengal CM Mamata",
        ],
        "kind": "person",
        "country": "india",
    },
    "Abhishek Banerjee": {
        "aliases": ["Abhishek Banerjee", "Abhishek", "TMC national general secretary"],
        "kind": "person",
        "country": "india",
    },
    "M. K. Stalin": {
        "aliases": [
            "M. K. Stalin",
            "Stalin",
            "MK Stalin",
            "CM Stalin",
            "Tamil Nadu CM Stalin",
        ],
        "kind": "person",
        "country": "india",
    },
    "Udhayanidhi Stalin": {
        "aliases": ["Udhayanidhi Stalin", "Udhayanidhi", "Udhay"],
        "kind": "person",
        "country": "india",
    },
    "Sharad Pawar": {
        "aliases": ["Sharad Pawar", "Pawar", "NCP chief Pawar"],
        "kind": "person",
        "country": "india",
    },
    "Ajit Pawar": {
        "aliases": ["Ajit Pawar", "Ajit", "Deputy CM Ajit Pawar"],
        "kind": "person",
        "country": "india",
    },
    "Uddhav Thackeray": {
        "aliases": ["Uddhav Thackeray", "Uddhav", "Thackeray"],
        "kind": "person",
        "country": "india",
    },
    "Eknath Shinde": {
        "aliases": ["Eknath Shinde", "Shinde", "CM Shinde", "Maharashtra CM Shinde"],
        "kind": "person",
        "country": "india",
    },
    "Devendra Fadnavis": {
        "aliases": ["Devendra Fadnavis", "Fadnavis", "CM Fadnavis"],
        "kind": "person",
        "country": "india",
    },
    "Akhilesh Yadav": {
        "aliases": [
            "Akhilesh Yadav",
            "Akhilesh",
            "SP chief Akhilesh",
            "Former UP CM Akhilesh",
        ],
        "kind": "person",
        "country": "india",
    },
    "Mulayam Singh Yadav": {
        "aliases": ["Mulayam Singh Yadav", "Mulayam", "Netaji"],
        "kind": "person",
        "country": "india",
    },
    "Mayawati": {
        "aliases": ["Mayawati", "Behenji", "BSP chief Mayawati", "Kumari Mayawati"],
        "kind": "person",
        "country": "india",
    },
    "Tejashwi Yadav": {
        "aliases": ["Tejashwi Yadav", "Tejashwi", "Bihar Deputy CM Tejashwi"],
        "kind": "person",
        "country": "india",
    },
    "Lalu Prasad Yadav": {
        "aliases": ["Lalu Prasad Yadav", "Lalu Prasad", "Lalu", "RJD chief Lalu"],
        "kind": "person",
        "country": "india",
    },
    "Nitish Kumar": {
        "aliases": ["Nitish Kumar", "Nitish", "Bihar CM Nitish", "CM Nitish Kumar"],
        "kind": "person",
        "country": "india",
    },
    "Chandrababu Naidu": {
        "aliases": [
            "Chandrababu Naidu",
            "Chandrababu",
            "Naidu",
            "TDP chief Naidu",
            "Andhra CM Naidu",
        ],
        "kind": "person",
        "country": "india",
    },
    "Y. S. Jagan Mohan Reddy": {
        "aliases": [
            "Y. S. Jagan Mohan Reddy",
            "Jagan Mohan Reddy",
            "Jagan",
            "YS Jagan",
            "YSRCP chief",
        ],
        "kind": "person",
        "country": "india",
    },
    "K. Chandrashekar Rao": {
        "aliases": [
            "K. Chandrashekar Rao",
            "KCR",
            "Chandrashekar Rao",
            "BRS chief KCR",
        ],
        "kind": "person",
        "country": "india",
    },
    "A. Revanth Reddy": {
        "aliases": [
            "A. Revanth Reddy",
            "Revanth Reddy",
            "Revanth",
            "Telangana CM Revanth",
        ],
        "kind": "person",
        "country": "india",
    },
    "Pinarayi Vijayan": {
        "aliases": ["Pinarayi Vijayan", "Pinarayi", "Kerala CM Pinarayi"],
        "kind": "person",
        "country": "india",
    },
    "Siddaramaiah": {
        "aliases": ["Siddaramaiah", "Karnataka CM Siddaramaiah", "CM Siddaramaiah"],
        "kind": "person",
        "country": "india",
    },
    "D. K. Shivakumar": {
        "aliases": ["D. K. Shivakumar", "DK Shivakumar", "DKS", "Karnataka Deputy CM"],
        "kind": "person",
        "country": "india",
    },
    "Hemant Soren": {
        "aliases": ["Hemant Soren", "Soren", "Jharkhand CM Hemant"],
        "kind": "person",
        "country": "india",
    },
    "Bhupesh Baghel": {
        "aliases": ["Bhupesh Baghel", "Baghel", "Former Chhattisgarh CM"],
        "kind": "person",
        "country": "india",
    },
    "Ashok Gehlot": {
        "aliases": ["Ashok Gehlot", "Gehlot", "Former Rajasthan CM Gehlot"],
        "kind": "person",
        "country": "india",
    },
    "Vasundhara Raje": {
        "aliases": [
            "Vasundhara Raje",
            "Vasundhara",
            "Raje",
            "Former Rajasthan CM Vasundhara",
        ],
        "kind": "person",
        "country": "india",
    },
    "Omar Abdullah": {
        "aliases": ["Omar Abdullah", "Omar", "J&K CM Omar", "NC leader Omar"],
        "kind": "person",
        "country": "india",
    },
    "Farooq Abdullah": {
        "aliases": ["Farooq Abdullah", "Farooq", "NC president Farooq"],
        "kind": "person",
        "country": "india",
    },
    "Mehbooba Mufti": {
        "aliases": ["Mehbooba Mufti", "Mehbooba", "PDP chief Mehbooba"],
        "kind": "person",
        "country": "india",
    },
    "Kapil Sibal": {
        "aliases": ["Kapil Sibal", "Sibal"],
        "kind": "person",
        "country": "india",
    },
    "P. Chidambaram": {
        "aliases": ["P. Chidambaram", "Chidambaram", "Former FM Chidambaram"],
        "kind": "person",
        "country": "india",
    },
    "Shashi Tharoor": {
        "aliases": ["Shashi Tharoor", "Tharoor"],
        "kind": "person",
        "country": "india",
    },
    "Smriti Irani": {
        "aliases": ["Smriti Irani", "Smriti", "Irani"],
        "kind": "person",
        "country": "india",
    },
    "Supriya Sule": {
        "aliases": ["Supriya Sule", "Supriya", "NCP MP Supriya"],
        "kind": "person",
        "country": "india",
    },
    "Chirag Paswan": {
        "aliases": ["Chirag Paswan", "Chirag", "LJP chief Chirag"],
        "kind": "person",
        "country": "india",
    },
    "Ram Vilas Paswan": {
        "aliases": ["Ram Vilas Paswan", "Ram Vilas", "LJP founder"],
        "kind": "person",
        "country": "india",
    },
    "Asaduddin Owaisi": {
        "aliases": ["Asaduddin Owaisi", "Owaisi", "AIMIM chief Owaisi"],
        "kind": "person",
        "country": "india",
    },
    "Sitaram Yechury": {
        "aliases": ["Sitaram Yechury", "Yechury", "CPI(M) general secretary"],
        "kind": "person",
        "country": "india",
    },
    "D. Raja": {
        "aliases": ["D. Raja", "D Raja", "CPI general secretary"],
        "kind": "person",
        "country": "india",
    },
    "Sudha Murthy": {
        "aliases": ["Sudha Murthy", "Sudha Murthy Rajya Sabha"],
        "kind": "person",
        "country": "india",
    },
    "Draupadi Murmu": {
        "aliases": ["Draupadi Murmu", "President Murmu", "Murmu"],
        "kind": "person",
        "country": "india",
    },
    "Ram Nath Kovind": {
        "aliases": ["Ram Nath Kovind", "Kovind", "Former President Kovind"],
        "kind": "person",
        "country": "india",
    },
    "Jagdeep Dhankhar": {
        "aliases": ["Jagdeep Dhankhar", "Dhankhar", "Vice President Dhankhar"],
        "kind": "person",
        "country": "india",
    },
    # INDIA – PARTIES
    "BJP": {
        "aliases": ["BJP", "Bharatiya Janata Party", "Bhartiya Janata Party"],
        "kind": "party",
        "country": "india",
    },
    "Congress": {
        "aliases": ["Congress", "INC", "Indian National Congress", "Grand Old Party"],
        "kind": "party",
        "country": "india",
    },
    "AAP": {
        "aliases": ["AAP", "Aam Aadmi Party", "Aam Admi Party"],
        "kind": "party",
        "country": "india",
    },
    "TMC": {
        "aliases": [
            "TMC",
            "Trinamool Congress",
            "All India Trinamool Congress",
            "AITC",
        ],
        "kind": "party",
        "country": "india",
    },
    "DMK": {
        "aliases": ["DMK", "Dravida Munnetra Kazhagam"],
        "kind": "party",
        "country": "india",
    },
    "AIADMK": {
        "aliases": ["AIADMK", "All India Anna Dravida Munnetra Kazhagam", "Anna DMK"],
        "kind": "party",
        "country": "india",
    },
    "NCP": {
        "aliases": [
            "NCP",
            "Nationalist Congress Party",
            "Sharad Pawar NCP",
            "NCP (SP)",
        ],
        "kind": "party",
        "country": "india",
    },
    "NCP (Ajit Pawar)": {
        "aliases": ["NCP Ajit Pawar", "NCP (Ajit)", "Ajit NCP"],
        "kind": "party",
        "country": "india",
    },
    "Shiv Sena (UBT)": {
        "aliases": [
            "Shiv Sena UBT",
            "Uddhav Sena",
            "Thackeray Sena",
            "Shiv Sena (Uddhav Balasaheb Thackeray)",
        ],
        "kind": "party",
        "country": "india",
    },
    "Shiv Sena (Shinde)": {
        "aliases": ["Shiv Sena Shinde", "Eknath Sena", "Shinde Sena"],
        "kind": "party",
        "country": "india",
    },
    "SP": {
        "aliases": ["SP", "Samajwadi Party", "Samajwadi"],
        "kind": "party",
        "country": "india",
    },
    "BSP": {
        "aliases": ["BSP", "Bahujan Samaj Party"],
        "kind": "party",
        "country": "india",
    },
    "RJD": {
        "aliases": ["RJD", "Rashtriya Janata Dal"],
        "kind": "party",
        "country": "india",
    },
    "JDU": {
        "aliases": ["JDU", "JD(U)", "Janata Dal United"],
        "kind": "party",
        "country": "india",
    },
    "JD(S)": {
        "aliases": ["JD(S)", "JDS", "Janata Dal Secular"],
        "kind": "party",
        "country": "india",
    },
    "TDP": {
        "aliases": ["TDP", "Telugu Desam Party", "Telugu Desam"],
        "kind": "party",
        "country": "india",
    },
    "YSR Congress": {
        "aliases": ["YSR Congress", "YSRCP", "YSR Congress Party", "Jagan party"],
        "kind": "party",
        "country": "india",
    },
    "BRS": {
        "aliases": [
            "BRS",
            "Bharat Rashtra Samithi",
            "TRS",
            "Telangana Rashtra Samithi",
            "KCR party",
        ],
        "kind": "party",
        "country": "india",
    },
    "CPI(M)": {
        "aliases": [
            "CPI(M)",
            "CPM",
            "Communist Party of India (Marxist)",
            "Communist Party Marxist",
        ],
        "kind": "party",
        "country": "india",
    },
    "CPI": {
        "aliases": ["CPI", "Communist Party of India"],
        "kind": "party",
        "country": "india",
    },
    "National Conference": {
        "aliases": [
            "National Conference",
            "NC",
            "Jammu and Kashmir National Conference",
            "J&K NC",
        ],
        "kind": "party",
        "country": "india",
    },
    "PDP": {
        "aliases": ["PDP", "Peoples Democratic Party", "J&K PDP"],
        "kind": "party",
        "country": "india",
    },
    "AIMIM": {
        "aliases": [
            "AIMIM",
            "All India Majlis-e-Ittehadul Muslimeen",
            "Majlis",
            "Owaisi party",
        ],
        "kind": "party",
        "country": "india",
    },
    "LJP": {
        "aliases": ["LJP", "Lok Janshakti Party", "LJP (Ram Vilas)"],
        "kind": "party",
        "country": "india",
    },
    "Apna Dal": {
        "aliases": ["Apna Dal", "Apna Dal (Sonelal)"],
        "kind": "party",
        "country": "india",
    },
    "INDIA Alliance": {
        "aliases": [
            "INDIA Alliance",
            "INDIA bloc",
            "I.N.D.I.A.",
            "Indian National Developmental Inclusive Alliance",
            "Opposition alliance",
        ],
        "kind": "party",
        "country": "india",
    },
    "NDA": {
        "aliases": ["NDA", "National Democratic Alliance", "NDA alliance"],
        "kind": "party",
        "country": "india",
    },
    "UPA": {
        "aliases": ["UPA", "United Progressive Alliance"],
        "kind": "party",
        "country": "india",
    },
    # INDIA – ISSUES / POLICIES / EVENTS
    "Demonetisation": {
        "aliases": [
            "Demonetisation",
            "demonetization",
            "demonetised",
            "demonetized",
            "notebandi",
            "note ban",
            "8 November 2016",
        ],
        "kind": "issue",
        "country": "india",
    },
    "GST": {
        "aliases": ["GST", "Goods and Services Tax", "goods & services tax"],
        "kind": "policy",
        "country": "india",
    },
    "CAA": {
        "aliases": [
            "CAA",
            "Citizenship Amendment Act",
            "Citizenship Amendment Bill",
            "CAB",
            "CAA-NRC",
        ],
        "kind": "policy",
        "country": "india",
    },
    "NRC": {
        "aliases": [
            "NRC",
            "National Register of Citizens",
            "National Citizens Register",
        ],
        "kind": "policy",
        "country": "india",
    },
    "Article 370": {
        "aliases": [
            "Article 370",
            "revocation of Article 370",
            "abrogation of Article 370",
            "Article 35A",
            "J&K special status",
        ],
        "kind": "issue",
        "country": "india",
    },
    "Ram Mandir": {
        "aliases": [
            "Ram Mandir",
            "Ayodhya temple",
            "Ram temple",
            "Ayodhya mandir",
            "Ram Janmabhoomi",
            "Babri Masjid verdict",
        ],
        "kind": "issue",
        "country": "india",
    },
    "Uniform Civil Code": {
        "aliases": ["Uniform Civil Code", "UCC", "common civil code"],
        "kind": "issue",
        "country": "india",
    },
    "Delimitation": {
        "aliases": [
            "delimitation",
            "constituency boundaries",
            "redrawing constituency boundaries",
            "delimitation commission",
        ],
        "kind": "issue",
        "country": "india",
    },
    "Women's Reservation Bill": {
        "aliases": [
            "women's reservation bill",
            "women reservation",
            "women's quota",
            "women quota",
            "33 per cent reservation",
            "Nari Shakti Vandan Adhiniyam",
        ],
        "kind": "issue",
        "country": "india",
    },
    "Farm Laws": {
        "aliases": [
            "farm laws",
            "agricultural laws",
            "farmers protest",
            "kisan andolan",
            "three farm laws",
            "farm reform laws",
        ],
        "kind": "issue",
        "country": "india",
    },
    "Electoral Bonds": {
        "aliases": [
            "electoral bonds",
            "electoral bond scheme",
            "political funding bonds",
        ],
        "kind": "issue",
        "country": "india",
    },
    "Agnipath Scheme": {
        "aliases": [
            "Agnipath",
            "Agnipath scheme",
            "Agniveer",
            "short-term military recruitment",
        ],
        "kind": "policy",
        "country": "india",
    },
    "Make in India": {
        "aliases": ["Make in India", "Make In India initiative"],
        "kind": "policy",
        "country": "india",
    },
    "Atmanirbhar Bharat": {
        "aliases": [
            "Atmanirbhar Bharat",
            "self-reliant India",
            "Aatmanirbhar Bharat",
            "self-sufficient India",
        ],
        "kind": "policy",
        "country": "india",
    },
    "Digital India": {
        "aliases": [
            "Digital India",
            "Digital India initiative",
            "digitisation of India",
        ],
        "kind": "policy",
        "country": "india",
    },
    "Aadhaar": {
        "aliases": [
            "Aadhaar",
            "Aadhar",
            "Aadhaar card",
            "UID",
            "Unique Identification",
        ],
        "kind": "policy",
        "country": "india",
    },
    "UPI": {
        "aliases": ["UPI", "Unified Payments Interface", "digital payments India"],
        "kind": "policy",
        "country": "india",
    },
    "MGNREGA": {
        "aliases": [
            "MGNREGA",
            "MNREGA",
            "Mahatma Gandhi National Rural Employment Guarantee Act",
            "rural employment guarantee scheme",
        ],
        "kind": "policy",
        "country": "india",
    },
    "National Education Policy": {
        "aliases": [
            "National Education Policy",
            "NEP",
            "NEP 2020",
            "new education policy",
        ],
        "kind": "policy",
        "country": "india",
    },
    "Triple Talaq": {
        "aliases": [
            "Triple Talaq",
            "instant triple talaq",
            "talaq-e-biddat",
            "Muslim women divorce law",
        ],
        "kind": "issue",
        "country": "india",
    },
    "OBC Reservation": {
        "aliases": [
            "OBC reservation",
            "OBC quota",
            "Other Backward Classes reservation",
            "backward caste reservation",
        ],
        "kind": "issue",
        "country": "india",
    },
    "EWS Reservation": {
        "aliases": [
            "EWS reservation",
            "EWS quota",
            "Economically Weaker Section reservation",
            "10 percent reservation",
            "general category reservation",
        ],
        "kind": "issue",
        "country": "india",
    },
    "Caste Census": {
        "aliases": [
            "caste census",
            "caste-based census",
            "caste enumeration",
            "OBC census",
        ],
        "kind": "issue",
        "country": "india",
    },
    "Pulwama Attack": {
        "aliases": [
            "Pulwama attack",
            "Pulwama",
            "Pulwama terror attack",
            "CRPF Pulwama",
        ],
        "kind": "event",
        "country": "india",
    },
    "Balakot Airstrike": {
        "aliases": [
            "Balakot airstrike",
            "Balakot strike",
            "surgical strike Balakot",
            "IAF Balakot",
        ],
        "kind": "event",
        "country": "india",
    },
    "One Nation One Election": {
        "aliases": [
            "One Nation One Election",
            "simultaneous elections",
            "ONOE",
            "one country one election",
        ],
        "kind": "issue",
        "country": "india",
    },
    "Bharat Jodo Yatra": {
        "aliases": [
            "Bharat Jodo Yatra",
            "Rahul Gandhi yatra",
            "Bharat Jodo",
            "Bharat Jodo Nyay Yatra",
        ],
        "kind": "event",
        "country": "india",
    },
    "India-China Border Dispute": {
        "aliases": [
            "India China border dispute",
            "Galwan valley clash",
            "LAC dispute",
            "Doklam standoff",
            "India-China standoff",
            "Arunachal Pradesh dispute",
        ],
        "kind": "issue",
        "country": "india",
    },
    "India-Pakistan Relations": {
        "aliases": [
            "India Pakistan relations",
            "India-Pakistan tensions",
            "cross-border terrorism",
            "LOC firing",
        ],
        "kind": "issue",
        "country": "india",
    },
    "Operation Sindoor": {
        "aliases": ["Operation Sindoor"],
        "kind": "event",
        "country": "india",
    },
    "Manipur Violence": {
        "aliases": [
            "Manipur violence",
            "Manipur ethnic clashes",
            "Manipur unrest",
            "Manipur conflict",
        ],
        "kind": "event",
        "country": "india",
    },
    "Adani Controversy": {
        "aliases": [
            "Adani controversy",
            "Hindenburg Adani",
            "Adani group controversy",
            "Adani stocks",
        ],
        "kind": "issue",
        "country": "india",
    },
    "PMLA": {
        "aliases": [
            "PMLA",
            "Prevention of Money Laundering Act",
            "money laundering act India",
        ],
        "kind": "policy",
        "country": "india",
    },
    "ED Raids": {
        "aliases": [
            "ED raids",
            "Enforcement Directorate raids",
            "ED action",
            "ED arrests",
        ],
        "kind": "issue",
        "country": "india",
    },
    "Pegasus Spyware": {
        "aliases": [
            "Pegasus spyware",
            "Pegasus snooping",
            "Pegasus surveillance India",
            "phone tapping India",
        ],
        "kind": "issue",
        "country": "india",
    },
    "General Elections 2024": {
        "aliases": [
            "General Elections 2024",
            "Lok Sabha elections 2024",
            "2024 elections",
            "Indian elections 2024",
            "Lok Sabha polls 2024",
        ],
        "kind": "event",
        "country": "india",
    },
    # US – PEOPLE
    "Donald Trump": {
        "aliases": [
            "Donald Trump",
            "Trump",
            "President Trump",
            "POTUS Trump",
            "DJT",
            "45th President",
            "47th President",
        ],
        "kind": "person",
        "country": "us",
    },
    "Joe Biden": {
        "aliases": [
            "Joe Biden",
            "Biden",
            "President Biden",
            "POTUS Biden",
            "46th President",
        ],
        "kind": "person",
        "country": "us",
    },
    "Kamala Harris": {
        "aliases": [
            "Kamala Harris",
            "Harris",
            "VP Harris",
            "Vice President Harris",
            "Madam Vice President",
        ],
        "kind": "person",
        "country": "us",
    },
    "Bernie Sanders": {
        "aliases": ["Bernie Sanders", "Bernie", "Sanders", "Senator Sanders"],
        "kind": "person",
        "country": "us",
    },
    "Alexandria Ocasio-Cortez": {
        "aliases": [
            "Alexandria Ocasio-Cortez",
            "AOC",
            "Ocasio-Cortez",
            "Congresswoman AOC",
        ],
        "kind": "person",
        "country": "us",
    },
    "Nancy Pelosi": {
        "aliases": [
            "Nancy Pelosi",
            "Pelosi",
            "Speaker Pelosi",
            "Former Speaker Pelosi",
        ],
        "kind": "person",
        "country": "us",
    },
    "Chuck Schumer": {
        "aliases": [
            "Chuck Schumer",
            "Schumer",
            "Senate Majority Leader Schumer",
            "Senator Schumer",
        ],
        "kind": "person",
        "country": "us",
    },
    "Mitch McConnell": {
        "aliases": [
            "Mitch McConnell",
            "McConnell",
            "Senate Minority Leader McConnell",
            "Senator McConnell",
        ],
        "kind": "person",
        "country": "us",
    },
    "Kevin McCarthy": {
        "aliases": ["Kevin McCarthy", "McCarthy", "Former Speaker McCarthy"],
        "kind": "person",
        "country": "us",
    },
    "Mike Johnson": {
        "aliases": ["Mike Johnson", "Speaker Johnson", "Speaker Mike Johnson"],
        "kind": "person",
        "country": "us",
    },
    "Ron DeSantis": {
        "aliases": [
            "Ron DeSantis",
            "DeSantis",
            "Governor DeSantis",
            "Florida Governor DeSantis",
        ],
        "kind": "person",
        "country": "us",
    },
    "Nikki Haley": {
        "aliases": ["Nikki Haley", "Haley", "Former Ambassador Haley", "Nimrata Haley"],
        "kind": "person",
        "country": "us",
    },
    "Vivek Ramaswamy": {
        "aliases": ["Vivek Ramaswamy", "Vivek", "Ramaswamy"],
        "kind": "person",
        "country": "us",
    },
    "JD Vance": {
        "aliases": [
            "JD Vance",
            "J.D. Vance",
            "Vance",
            "Vice President Vance",
            "Senator Vance",
        ],
        "kind": "person",
        "country": "us",
    },
    "Marco Rubio": {
        "aliases": [
            "Marco Rubio",
            "Rubio",
            "Senator Rubio",
            "Secretary of State Rubio",
        ],
        "kind": "person",
        "country": "us",
    },
    "Ted Cruz": {
        "aliases": ["Ted Cruz", "Cruz", "Senator Cruz"],
        "kind": "person",
        "country": "us",
    },
    "Rand Paul": {
        "aliases": ["Rand Paul", "Paul", "Senator Rand Paul"],
        "kind": "person",
        "country": "us",
    },
    "Lindsey Graham": {
        "aliases": ["Lindsey Graham", "Graham", "Senator Graham"],
        "kind": "person",
        "country": "us",
    },
    "Elizabeth Warren": {
        "aliases": ["Elizabeth Warren", "Warren", "Senator Warren"],
        "kind": "person",
        "country": "us",
    },
    "Pete Buttigieg": {
        "aliases": ["Pete Buttigieg", "Buttigieg", "Mayor Pete", "Secretary Buttigieg"],
        "kind": "person",
        "country": "us",
    },
    "Barack Obama": {
        "aliases": ["Barack Obama", "Obama", "President Obama", "44th President"],
        "kind": "person",
        "country": "us",
    },
    "Hillary Clinton": {
        "aliases": [
            "Hillary Clinton",
            "Hillary",
            "Clinton",
            "Former Secretary Clinton",
        ],
        "kind": "person",
        "country": "us",
    },
    "Mike Pence": {
        "aliases": ["Mike Pence", "Pence", "Former VP Pence", "Vice President Pence"],
        "kind": "person",
        "country": "us",
    },
    "Gavin Newsom": {
        "aliases": [
            "Gavin Newsom",
            "Newsom",
            "Governor Newsom",
            "California Governor Newsom",
        ],
        "kind": "person",
        "country": "us",
    },
    "Gretchen Whitmer": {
        "aliases": [
            "Gretchen Whitmer",
            "Whitmer",
            "Governor Whitmer",
            "Michigan Governor Whitmer",
        ],
        "kind": "person",
        "country": "us",
    },
    "Josh Shapiro": {
        "aliases": [
            "Josh Shapiro",
            "Shapiro",
            "Governor Shapiro",
            "Pennsylvania Governor",
        ],
        "kind": "person",
        "country": "us",
    },
    "Tim Walz": {
        "aliases": ["Tim Walz", "Walz", "Governor Walz", "Coach Walz"],
        "kind": "person",
        "country": "us",
    },
    "Elon Musk": {
        "aliases": [
            "Elon Musk",
            "Musk",
            "DOGE chief Musk",
            "Department of Government Efficiency Musk",
        ],
        "kind": "person",
        "country": "us",
    },
    "Steve Bannon": {
        "aliases": ["Steve Bannon", "Bannon"],
        "kind": "person",
        "country": "us",
    },
    "Rudy Giuliani": {
        "aliases": ["Rudy Giuliani", "Giuliani", "Former Mayor Giuliani"],
        "kind": "person",
        "country": "us",
    },
    "Ilhan Omar": {
        "aliases": [
            "Ilhan Omar",
            "Omar",
            "Congresswoman Ilhan Omar",
            "Representative Omar",
        ],
        "kind": "person",
        "country": "us",
    },
    "Rashida Tlaib": {
        "aliases": ["Rashida Tlaib", "Tlaib", "Representative Tlaib"],
        "kind": "person",
        "country": "us",
    },
    "Adam Schiff": {
        "aliases": ["Adam Schiff", "Schiff", "Representative Schiff", "Senator Schiff"],
        "kind": "person",
        "country": "us",
    },
    "Jim Jordan": {
        "aliases": ["Jim Jordan", "Jordan", "Representative Jim Jordan"],
        "kind": "person",
        "country": "us",
    },
    "Matt Gaetz": {
        "aliases": ["Matt Gaetz", "Gaetz", "Representative Gaetz"],
        "kind": "person",
        "country": "us",
    },
    "Marjorie Taylor Greene": {
        "aliases": ["Marjorie Taylor Greene", "MTG", "Greene", "Representative Greene"],
        "kind": "person",
        "country": "us",
    },
    "Pete Hegseth": {
        "aliases": [
            "Pete Hegseth",
            "Hegseth",
            "Secretary Hegseth",
            "Defense Secretary Hegseth",
        ],
        "kind": "person",
        "country": "us",
    },
    "Robert F. Kennedy Jr.": {
        "aliases": [
            "Robert F. Kennedy Jr.",
            "RFK Jr.",
            "RFK",
            "Kennedy Jr.",
            "HHS Secretary Kennedy",
        ],
        "kind": "person",
        "country": "us",
    },
    # US – PARTIES
    "Republican Party": {
        "aliases": ["Republican Party", "Republicans", "GOP", "Grand Old Party"],
        "kind": "party",
        "country": "us",
    },
    "Democratic Party": {
        "aliases": [
            "Democratic Party",
            "Democrats",
            "Dems",
            "Democratic National Committee",
            "DNC",
        ],
        "kind": "party",
        "country": "us",
    },
    "Green Party": {
        "aliases": ["Green Party", "Green Party US", "Greens"],
        "kind": "party",
        "country": "us",
    },
    "Libertarian Party": {
        "aliases": ["Libertarian Party", "Libertarians"],
        "kind": "party",
        "country": "us",
    },
    "MAGA": {
        "aliases": [
            "MAGA",
            "Make America Great Again",
            "MAGA movement",
            "MAGA Republicans",
            "Trump Republicans",
        ],
        "kind": "party",
        "country": "us",
    },
    "Progressive Caucus": {
        "aliases": [
            "Progressive Caucus",
            "Congressional Progressive Caucus",
            "Squad",
            "The Squad",
            "progressives",
        ],
        "kind": "party",
        "country": "us",
    },
    "Freedom Caucus": {
        "aliases": ["Freedom Caucus", "House Freedom Caucus", "conservative caucus"],
        "kind": "party",
        "country": "us",
    },
    # US – ISSUES / POLICIES / EVENTS
    "Abortion Rights": {
        "aliases": [
            "abortion rights",
            "abortion ban",
            "Roe v. Wade",
            "Roe v Wade",
            "pro-choice",
            "pro-life",
            "reproductive rights",
            "Dobbs decision",
        ],
        "kind": "issue",
        "country": "us",
    },
    "Gun Control": {
        "aliases": [
            "gun control",
            "gun reform",
            "gun violence",
            "gun laws",
            "Second Amendment",
            "assault weapons ban",
            "background checks guns",
        ],
        "kind": "issue",
        "country": "us",
    },
    "Immigration": {
        "aliases": [
            "immigration",
            "illegal immigration",
            "border security",
            "undocumented immigrants",
            "DACA",
            "Dreamers",
            "southern border",
            "border wall",
            "migrant crisis",
        ],
        "kind": "issue",
        "country": "us",
    },
    "Affordable Care Act": {
        "aliases": [
            "Affordable Care Act",
            "ACA",
            "Obamacare",
            "healthcare reform",
            "health insurance mandate",
        ],
        "kind": "policy",
        "country": "us",
    },
    "Student Loan Debt": {
        "aliases": [
            "student loan debt",
            "student loan forgiveness",
            "student debt cancellation",
            "college debt",
        ],
        "kind": "issue",
        "country": "us",
    },
    "Climate Change": {
        "aliases": [
            "climate change",
            "global warming",
            "climate crisis",
            "Paris Agreement",
            "Green New Deal",
            "climate policy",
            "carbon emissions",
        ],
        "kind": "issue",
        "country": "us",
    },
    "January 6 Capitol Attack": {
        "aliases": [
            "January 6",
            "January 6th",
            "Capitol attack",
            "Capitol riot",
            "Capitol insurrection",
            "J6",
            "storming the Capitol",
        ],
        "kind": "event",
        "country": "us",
    },
    "Trump Impeachment": {
        "aliases": [
            "Trump impeachment",
            "first impeachment",
            "second impeachment",
            "impeachment trial",
            "impeachment of Trump",
        ],
        "kind": "event",
        "country": "us",
    },
    "Trump Indictment": {
        "aliases": [
            "Trump indictment",
            "Trump criminal case",
            "Trump trial",
            "Trump federal charges",
            "Trump hush money trial",
            "Trump Georgia case",
        ],
        "kind": "event",
        "country": "us",
    },
    "Inflation": {
        "aliases": [
            "inflation",
            "cost of living",
            "price hike",
            "consumer prices",
            "inflation crisis",
        ],
        "kind": "issue",
        "country": "us",
    },
    "Inflation Reduction Act": {
        "aliases": [
            "Inflation Reduction Act",
            "IRA",
            "climate bill",
            "Biden climate law",
        ],
        "kind": "policy",
        "country": "us",
    },
    "CHIPS Act": {
        "aliases": [
            "CHIPS Act",
            "CHIPS and Science Act",
            "semiconductor bill",
            "chip manufacturing law",
        ],
        "kind": "policy",
        "country": "us",
    },
    "Ukraine War": {
        "aliases": [
            "Ukraine war",
            "Russia Ukraine war",
            "war in Ukraine",
            "Ukraine conflict",
            "Ukraine aid",
            "Russia invasion of Ukraine",
        ],
        "kind": "issue",
        "country": "us",
    },
    "Israel Gaza": {
        "aliases": [
            "Israel Gaza",
            "Gaza war",
            "Israel Hamas war",
            "Gaza conflict",
            "Middle East conflict",
            "Israel Palestine",
        ],
        "kind": "issue",
        "country": "us",
    },
    "Tariffs": {
        "aliases": [
            "tariffs",
            "trade tariffs",
            "import tariffs",
            "Trump tariffs",
            "trade war",
            "reciprocal tariffs",
            "China tariffs",
        ],
        "kind": "issue",
        "country": "us",
    },
    "DEI": {
        "aliases": [
            "DEI",
            "diversity equity and inclusion",
            "diversity equity inclusion",
            "affirmative action",
            "DEI programs",
        ],
        "kind": "issue",
        "country": "us",
    },
    "Social Security": {
        "aliases": [
            "Social Security",
            "Social Security benefits",
            "retirement benefits",
            "Social Security cuts",
        ],
        "kind": "policy",
        "country": "us",
    },
    "Medicare": {
        "aliases": ["Medicare", "Medicare for All", "senior health insurance"],
        "kind": "policy",
        "country": "us",
    },
    "Medicaid": {
        "aliases": ["Medicaid", "low-income healthcare", "Medicaid cuts"],
        "kind": "policy",
        "country": "us",
    },
    "Tax Cuts and Jobs Act": {
        "aliases": ["Tax Cuts and Jobs Act", "Trump tax cuts", "TCJA", "2017 tax law"],
        "kind": "policy",
        "country": "us",
    },
    "DOGE": {
        "aliases": [
            "DOGE",
            "Department of Government Efficiency",
            "Musk DOGE",
            "government efficiency cuts",
        ],
        "kind": "policy",
        "country": "us",
    },
    "2020 Election": {
        "aliases": [
            "2020 election",
            "2020 presidential election",
            "election fraud 2020",
            "stolen election",
            "2020 election results",
        ],
        "kind": "event",
        "country": "us",
    },
    "2024 Election": {
        "aliases": [
            "2024 election",
            "2024 presidential election",
            "2024 US election",
            "presidential race 2024",
        ],
        "kind": "event",
        "country": "us",
    },
    "Supreme Court": {
        "aliases": [
            "Supreme Court",
            "SCOTUS",
            "Supreme Court ruling",
            "Supreme Court decision",
        ],
        "kind": "issue",
        "country": "us",
    },
    "Filibuster": {
        "aliases": [
            "filibuster",
            "Senate filibuster",
            "ending the filibuster",
            "nuclear option",
        ],
        "kind": "issue",
        "country": "us",
    },
    "Debt Ceiling": {
        "aliases": [
            "debt ceiling",
            "debt limit",
            "government shutdown",
            "debt ceiling crisis",
        ],
        "kind": "issue",
        "country": "us",
    },
}


def load_registry_from_json(path: str) -> Dict[str, Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_entry(
    registry: Dict[str, Dict[str, Any]], canonical_target: str
) -> Dict[str, Any]:
    return registry.get(canonical_target, {})


def get_aliases(
    registry: Dict[str, Dict[str, Any]], canonical_target: str
) -> List[str]:
    entry = get_entry(registry, canonical_target)
    aliases = entry.get("aliases", [])
    vals = [canonical_target] + aliases
    seen = set()
    out = []
    for x in vals:
        xl = x.lower()
        if xl not in seen:
            seen.add(xl)
            out.append(x)
    return out


# won't be using related!
def get_related(
    registry: Dict[str, Dict[str, Any]], canonical_target: str
) -> List[str]:
    entry = get_entry(registry, canonical_target)
    return entry.get("related", [])


def resolve_target(
    raw_target: str, registry: Optional[Dict[str, Dict[str, Any]]] = None
) -> str:
    """
    Map a raw target like 'Modi' or 'Didi' to the canonical key if found.
    Falls back to the raw target unchanged.
    """
    if registry is None:
        return raw_target

    if raw_target in registry:
        return raw_target

    raw_low = raw_target.strip().lower()
    for canonical, meta in registry.items():
        if raw_low == canonical.lower():
            return canonical
        for alias in meta.get("aliases", []):
            if raw_low == alias.lower():
                return canonical

    return raw_target
