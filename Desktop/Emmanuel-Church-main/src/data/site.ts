export type LinkItem = {
  label: string;
  href: string;
  external?: boolean;
  description?: string;
};

export type StaffMember = {
  name: string;
  role: string;
  email?: string;
  image: string;
  note?: string;
};

export const site = {
  name: "Emmanuel Church",
  tagline: "A gospel-centered church in Abilene, for Abilene.",
  mission:
    "To see people transformed and families strengthened through the love, grace, worship, and truth of Jesus Christ.",
  phone: "(785) 263-3342",
  address: "1300 N. Vine Street, Abilene, KS 67410",
  mapHref:
    "https://www.google.com/maps/place/Emmanuel+Church/@38.9200234,-97.232936,15z/data=!4m5!3m4!1s0x87bcf07e5686bfb7:0x285057d82a83c28f!8m2!3d38.9287299!4d-97.2237321",
  mapEmbedHref:
    "https://www.google.com/maps?q=Emmanuel%20Church%2C%201300%20N.%20Vine%20Street%2C%20Abilene%2C%20KS%2067410&output=embed",
  facebook: "https://www.facebook.com/ecabilene/",
  onlineChurch: "https://emmanuelchurchabilene.online.church/",
  givingHref: "https://www.fellowshiponegiving.com/App/Giving/ecabilene",
  calendarHref:
    "https://emmanuel.fellowshiponego.com/calendar/calendar_public/embeded/45cbaa3ef777e9a92378912fec818fa8#month",
  bibleApp: "http://www.bible.com",
};

export const primaryNav: LinkItem[] = [
  { label: "About", href: "/worship/who-we-are" },
  { label: "Ministries", href: "/connect" },
  { label: "Sermons", href: "/resources/sermons" },
  { label: "Events", href: "/resources/church-calendar" },
  { label: "Give", href: "/resources/online-giving" },
  { label: "Contact", href: "/contact" },
];

export const quickLinks: LinkItem[] = [
  {
    label: "Plan Your Visit",
    href: "/contact",
    description: "Start with the front door, service times, and location.",
  },
  {
    label: "Watch Latest Sermon",
    href: "/resources/live-stream",
    description: "Go straight to the live stream and sermon platform.",
  },
  {
    label: "View Calendar",
    href: "/resources/church-calendar",
    description: "See the public church calendar and upcoming gatherings.",
  },
  {
    label: "Give Online",
    href: "/resources/online-giving",
    description: "Open the current online giving portal.",
  },
];

export const featureCards = [
  {
    title: "Expository Preaching",
    text: "Scripture drives the message.",
    href: "/resources/sermons",
  },
  {
    title: "Gospel Community",
    text: "Belong, grow, and serve together.",
    href: "/connect",
  },
  {
    title: "Generous Giving",
    text: "Support the ministry God is building.",
    href: "/resources/online-giving",
  },
  {
    title: "Upcoming Events",
    text: "Stay close to the life of the church.",
    href: "/resources/church-calendar",
  },
];

export const serviceRhythm = [
  {
    label: "First Service",
    value: "8:45am",
    detail: "Traditional service with hymns and liturgy.",
  },
  {
    label: "Discipleship Hour",
    value: "10:00am - 10:45am",
    detail: "Classes for children, students, and adults.",
  },
  {
    label: "Second Service",
    value: "11:00am",
    detail: "Contemporary worship with a blended feel.",
  },
  {
    label: "Family Care",
    value: "Nursing Mothers Room 210",
    detail: "Nursery support and stream access for young families.",
  },
];

export const ministryLinks: LinkItem[] = [
  {
    label: "Emmanuel Preschool",
    href: "/connect/emmanuel-preschool",
    description: "Christ-centered learning for ages 3-5.",
  },
  {
    label: "Emmanuel Kids",
    href: "/connect/emmanuel-kids",
    description: "A joyful place for children to grow in faith.",
  },
  {
    label: "Momentum Youth",
    href: "/connect/momentum-youth",
    description: "Middle and high school students grounded in Scripture.",
  },
  {
    label: "Adult Discipleship Groups",
    href: "/connect/adult-discipleship-groups",
    description: "Biblical study, prayer, and shared life for adults.",
  },
  {
    label: 'Wednesday Night "B.L.A.S.T."',
    href: "/connect/wednesday-night-blast",
    description: "Midweek gathering for children, students, and families.",
  },
  {
    label: "Worship Arts Ministry",
    href: "/connect/worship-arts-ministry",
    description: "Music and technical support that serve gathered worship.",
  },
];

export const resourceLinks: LinkItem[] = [
  { label: "Church Calendar", href: "/resources/church-calendar" },
  { label: "Online Giving", href: "/resources/online-giving" },
  { label: "LIVE STREAM", href: "/resources/live-stream" },
  { label: "Sermons", href: "/resources/sermons" },
  { label: "Weekly Sermon Study Guides", href: "/resources/weekly-sermon-study-guides" },
  { label: "Bulletin", href: "/resources/bulletin" },
  { label: "Online Forms", href: "/resources/online-forms" },
  { label: "Spiritual Gifts / Serve Booklet", href: "/resources/spiritual-gifts-serve-booklet" },
  { label: "Fellowship One Go", href: "/resources/fellowship-one-go" },
  { label: "Emmanuel Partners", href: "/resources/emmanuel-partners" },
];

export const whoWeAreValues = [
  {
    title: "Love",
    body:
      "Love shapes the posture of the church and the way we serve one another.",
  },
  {
    title: "Grace",
    body:
      "Grace is God's undeserved gift, made clear in Jesus Christ.",
  },
  {
    title: "Worship",
    body:
      "Worship is our response of praise, prayer, generosity, and surrender.",
  },
  {
    title: "Truth",
    body:
      "God's truth is revealed by the Holy Spirit and lived out with confidence.",
  },
];

export const staff: StaffMember[] = [
  {
    name: "Marc Riegel",
    role: "Lead Pastor",
    email: "mriegel@ecabilene.org",
    image: "/staff/Marc-Riegel-Lead-Pastor.png",
  },
  {
    name: "Laura Ediger",
    role: "Worship Arts Pastor",
    email: "lediger@ecabilene.org",
    image: "/staff/Laura-Ediger-Worship-Arts-Pastor.png",
  },
  {
    name: "Shawn Ammons",
    role: "Youth Pastor",
    email: "shawnammons@infaith.org",
    image: "/staff/Shawn-Ammons-Youth-Pastor.png",
  },
  {
    name: "Rachel Bishop",
    role: "Kid's Pastor & Preschool Director",
    email: "rbishop@ecabilene.org",
    image: "/staff/Rachel-Bishop-Kid-s-Pastor-Preschool-Director.png",
  },
  {
    name: "Pam Rothfuss",
    role: "Financial Administrator",
    email: "prothfuss@ecabilene.org",
    image: "/staff/Pam-Rothfuss-Financial-Administrator.png",
  },
  {
    name: "Sheila Waldrop",
    role: "Administrative Assistant",
    email: "swaldrop@ecabilene.org",
    image: "/staff/Sheila-Waldrop-Administrative-Assistant.jpeg",
  },
  {
    name: "Marie Malo",
    role: "Preschool Teacher",
    email: "preschool@ecabilene.org",
    image: "/staff/Marie-Malo-Preschool-Teacher.jpeg",
  },
  {
    name: "Jonathan Beyard",
    role: "Grounds and Maintenance Supervisor",
    image: "/staff/Jonathan-Beyard-Grounds-and-Maintenance-Supervisor.jpeg",
  },
  {
    name: "Phil Watson",
    role: "Custodian",
    image: "/staff/Phil-Watson-Custodian.png",
  },
  {
    name: "Danielle Ridder",
    role: "Custodian",
    image: "/staff/Danielle-Ridder-Custodian.png",
  },
];

export const contactEmails = [
  "mriegel@ecabilene.org",
  "lediger@ecabilene.org",
  "shawnammons@infaith.org",
  "rbishop@ecabilene.org",
  "prothfuss@ecabilene.org",
  "swaldrop@ecabilene.org",
  "preschool@ecabilene.org",
];

export const externalLinks = [
  {
    label: "Facebook",
    href: site.facebook,
    note: "Primary public social channel.",
  },
  {
    label: "Online Church Platform",
    href: site.onlineChurch,
    note: "Current live-stream destination.",
  },
  {
    label: "Online Giving",
    href: site.givingHref,
    note: "Current donation portal.",
  },
  {
    label: "Public Calendar",
    href: site.calendarHref,
    note: "Public church calendar embed.",
  },
];

export const sermonArchive: LinkItem[] = [
  {
    label: "Walk As Jesus Walked",
    href: "http://www.ecabilene.org/media/777099-3763930-35171550/walk-as-jesus-walked",
  },
  {
    label: "Week 1 - Understanding Foundations of Wesleyan Theology",
    href: "http://www.ecabilene.org/media/777099-4848052-32718176/week-1-understanding-foundations-of-wesleyan-theology",
  },
  {
    label: "Polka-Dotted Christianity and ACCOUNTABILITY",
    href: "http://www.ecabilene.org/media/777099-3565774-2407869/polka-dotted-christianity-and-accountability",
  },
  {
    label: "Sunday Evening: James Murunga Service",
    href: "http://www.ecabilene.org/media/777099-3552169-2402890/sunday-evening-james-murunga-service",
  },
  {
    label: "Polka-Dotted Christianity and EVANGELISM",
    href: "http://www.ecabilene.org/media/777099-3552226-2402921/polka-dotted-christianity-and-evangelism",
  },
  {
    label: "Polka Dotted Christianity and the CHURCH",
    href: "http://www.ecabilene.org/media/777099-3542092-2392538/polka-dotted-christianity-and-the-church",
  },
  {
    label: "Coffee WITH: Staff and Spouses",
    href: "http://www.ecabilene.org/media/777099-3532997-2384005/coffee-with-staff-and-spouses",
  },
  {
    label: "Legacy",
    href: "http://www.ecabilene.org/media/777099-3523563-2372095/legacy",
  },
  {
    label: "Marriage",
    href: "http://www.ecabilene.org/media/777099-3507203-2363971/marriage",
  },
  {
    label: "FAMILY",
    href: "http://www.ecabilene.org/media/777099-3507208-2352515/family",
  },
  {
    label: "WORSHIP & TRUTH",
    href: "http://www.ecabilene.org/media/777099-3486873-2330042/worship-truth",
  },
  {
    label: "LOVE & GRACE",
    href: "http://www.ecabilene.org/media/777099-3471819-2310999/love-grace",
  },
  {
    label: "Road, Reflection, & Renewal",
    href: "http://www.ecabilene.org/media/777099-3716380-2537434/road-reflection-renewal",
  },
  {
    label: "Yearly Goals",
    href: "http://www.ecabilene.org/media/777099-3462905-2293865/yearly-goals",
  },
  {
    label: "Shaken to the Core: Calling",
    href: "http://www.ecabilene.org/media/777099-3455643-2277645/shaken-to-the-core-calling",
  },
  {
    label: "One Way: The Cradle to Cross to Grave to Heaven",
    href: "http://www.ecabilene.org/media/777099-3443324-2269812/one-way-the-cradle-to-cross-to-grave-to-heaven",
  },
  {
    label: "Detour: God with Us",
    href: "http://www.ecabilene.org/media/777099-3438026-2250922/detour-god-with-us",
  },
  {
    label: "The Signs of Christmas: Baby on Board",
    href: "http://www.ecabilene.org/media/777099-3434277-2237823/the-signs-of-christmas-baby-on-board",
  },
  {
    label: "Road Work Ahead: The Prophesies of a Messiah",
    href: "http://www.ecabilene.org/media/777099-3427475-2224862/road-work-ahead-the-prophesies-of-a-messiah",
  },
  {
    label: 'VOX: Week 4 - "Contented"',
    href: "http://www.ecabilene.org/media/777099-3422239-2211626/vox-week-4-contented",
  },
  {
    label: "VOX: CONFIRMATION",
    href: "http://www.ecabilene.org/media/777099-3414261-2197036/vox-confirmation",
  },
  {
    label: "James Murunga Evening Prayer Service",
    href: "http://www.ecabilene.org/media/777099-3409432-2186136/james-murunga-evening-prayer-service",
  },
  {
    label: "VOX: Conversation (Week 2)",
    href: "http://www.ecabilene.org/media/777099-3409340-2186077/vox-conversation-week-2",
  },
  {
    label: "VOX: Call (Week 1)",
    href: "http://www.ecabilene.org/media/777099-3399403-2169805/vox-call-week-1",
  },
  {
    label: "Real Steel: Sword of the Spirit, Week 4",
    href: "http://www.ecabilene.org/media/777099-3394268-2160089/real-steel-sword-of-the-spirit-week-4",
  },
  {
    label: "Real Steel: Shield & Helmet, Week 3",
    href: "http://www.ecabilene.org/media/777099-3394267-2160086/real-steel-shield-helmet-week-3",
  },
  {
    label: "Real Steel - Breastplate & Shoes",
    href: "http://www.ecabilene.org/media/777099-3374275-2122101/real-steel-breastplate-shoes",
  },
  {
    label: "Real Steel: Intro & Belt of Truth",
    href: "http://www.ecabilene.org/media/777099-3368482-2107469/real-steel-intro-belt-of-truth",
  },
  {
    label: "Kids Serve Sunday",
    href: "http://www.ecabilene.org/media/777099-3358317-2088758/kids-serve-sunday",
  },
  {
    label: "GOLDILOCKS: The Art of Balancing GRACE and TRUTH - Week 3",
    href: "http://www.ecabilene.org/media/777099-3351179-2075407/goldilocks-the-art-of-balancing-grace-and-truth-week-3",
  },
  {
    label: "GOLDILOCKS: The Art of Balancing GRACE and TRUTH - Week 2",
    href: "http://www.ecabilene.org/media/777099-3340988-2057929/goldilocks-the-art-of-balancing-grace-and-truth-week-2",
  },
  {
    label: "Goldilocks: The Art of Balancing Grace and Truth, Week 1",
    href: "http://www.ecabilene.org/media/777099-3334167-2048794/goldilocks-the-art-of-balancing-grace-and-truth-week-1",
  },
  {
    label: "Coffee WITH: Thomas Bishop",
    href: "http://www.ecabilene.org/media/777099-3334162-2048387/coffee-with-thomas-bishop",
  },
  {
    label: 'REVIVE: "The Future" Week 3',
    href: "http://www.ecabilene.org/media/777099-3317672-2024265/revive-the-future-week-3",
  },
  {
    label: 'REVIVE: "The Past" Week 2',
    href: "http://www.ecabilene.org/media/777099-3317612-2024252/revive-the-past-week-2",
  },
  {
    label: 'REVIVE: "The Past" Week 1',
    href: "http://www.ecabilene.org/media/777099-3296557-2002187/revive-the-past-week-1",
  },
  {
    label: "Father's Day Panel",
    href: "http://www.ecabilene.org/media/777099-3231972-1930683/fathers-day-panel",
  },
  {
    label: '"Halal & Zamar"',
    href: "http://www.ecabilene.org/media/777099-3231973-1930682/halal-zamar",
  },
];
