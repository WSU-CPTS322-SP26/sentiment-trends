import bitcoin from "../assets/bitcoin.png";
import openai from "../assets/openai.png";
import taylor_swift from "../assets/taylor_swift.png";
import super_bowl from "../assets/super_bowl.png";
import apple from "../assets/apple.png";
import tesla from "../assets/tesla.png";
import sp500 from "../assets/sp500.png";
import billie_eilish from "../assets/billie_eilish.png";
import amazon from "../assets/amazon.png";

export const mockSearch = [
  { id: 1, term: "Super Bowl LX"},
  { id: 2, term: "OpenAI"},
  { id: 3, term: "Taylor Swift"},
  { id: 4, term: "Winter Olympics 2026"},
  { id: 5, term: "Donald Trump"},
  { id: 6, term: "Elon Musk"},
  { id: 7, term: "Billie Eilish"},
  { id: 8, term: "Puppy Bowl XXII"},
  { id: 9, term: "World Cup 2026"},
  { id: 10, term: "Apple Inc."},
  { id: 11, term: "Amazon"},
  { id: 12, term: "Bitcoin"},
  { id: 13, term: "Meta"},
  { id: 14, term: "Steam Deck"},
  { id: 15, term: "Steph Curry"},
  { id: 16, term: "S&P 500"},
  { id: 17, term: "Tesla"},
  { id: 18, term: "iPhone 18 Pro"},
  { id: 19, term: "Quantum Computing"},
  { id: 20, term: "Lebron James"},
  { id: 21, term: "Venmo"},
];

export const mockCards = [
  {
    id: 1,
    title: "Bitcoin",
    image: bitcoin,
    negative_sentiment: 0.4,
    neutral_sentiment: 0.3,
    positive_sentiment: 0.3,
    compound_sentiment: 0.0
  },
  {
    id: 2,
    title: "OpenAI",
    image: openai,
    negative_sentiment: 0.4,
    neutral_sentiment: 0.4,
    positive_sentiment: 0.2,
    compound_sentiment: -0.2
  },
  {
    id: 3,
    title: "Taylor Swift",
    image: taylor_swift,
    negative_sentiment: 0.2,
    neutral_sentiment: 0.3,
    positive_sentiment: 0.5,
    compound_sentiment: 0.3
  },
  {
    id: 4,
    title: "Super Bowl LX",
    image: super_bowl,
    negative_sentiment: 0.1,
    neutral_sentiment: 0.2,
    positive_sentiment: 0.7,
    compound_sentiment: 0.5
  },
  {
    id: 5,
    title: "Apple",
    image: apple,
    negative_sentiment: 0.3,
    neutral_sentiment: 0.4,
    positive_sentiment: 0.3,
    compound_sentiment: 0.0
  },
  {
    id: 6,
    title: "Tesla",
    image: tesla,
    negative_sentiment: 0.5,
    neutral_sentiment: 0.3,
    positive_sentiment: 0.2,
    compound_sentiment: -0.3
  },
  {
    id: 7,
    title: "S&P 500",
    image: sp500,
    negative_sentiment: 0.2,
    neutral_sentiment: 0.3,
    positive_sentiment: 0.5,
    compound_sentiment: 0.3
  },
  {
    id: 8,
    title: "Billie Eilish",
    image: billie_eilish,
    negative_sentiment: 0.1,
    neutral_sentiment: 0.2,
    positive_sentiment: 0.7,
    compound_sentiment: 0.5
  },
  {
    id: 9,
    title: "Amazon",
    image: amazon,
    negative_sentiment: 0.4,
    neutral_sentiment: 0.4,
    positive_sentiment: 0.2,
    compound_sentiment: -0.2
  },
  {
    id: 10,
    title: "Bitcoin",
    image: bitcoin,
    negative_sentiment: 0.4,
    neutral_sentiment: 0.3,
    positive_sentiment: 0.3,
    compound_sentiment: 0.0
  },
  {
    id: 11,
    title: "OpenAI",
    image: openai,
    negative_sentiment: 0.4,
    neutral_sentiment: 0.4,
    positive_sentiment: 0.2,
    compound_sentiment: -0.2
  },
  {
    id: 12,
    title: "Taylor Swift",
    image: taylor_swift,
    negative_sentiment: 0.2,
    neutral_sentiment: 0.3,
    positive_sentiment: 0.5,
    compound_sentiment: 0.3
  },
  {
    id: 13,
    title: "Super Bowl LX",
    image: super_bowl,
    negative_sentiment: 0.1,
    neutral_sentiment: 0.2,
    positive_sentiment: 0.7,
    compound_sentiment: 0.5
  },
  {
    id: 14,
    title: "Apple",
    image: apple,
    negative_sentiment: 0.3,
    neutral_sentiment: 0.4,
    positive_sentiment: 0.3,
    compound_sentiment: 0.0
  },
  {
    id: 15,
    title: "Tesla",
    image: tesla,
    negative_sentiment: 0.5,
    neutral_sentiment: 0.3,
    positive_sentiment: 0.2,
    compound_sentiment: -0.3
  },
  {
    id: 16,
    title: "S&P 500",
    image: sp500,
    negative_sentiment: 0.2,
    neutral_sentiment: 0.3,
    positive_sentiment: 0.5,
    compound_sentiment: 0.3
  },
  {
    id: 17,
    title: "Billie Eilish",
    image: billie_eilish,
    negative_sentiment: 0.1,
    neutral_sentiment: 0.2,
    positive_sentiment: 0.7,
    compound_sentiment: 0.5
  },
  {
    id: 18,
    title: "Amazon",
    image: amazon,
    negative_sentiment: 0.4,
    neutral_sentiment: 0.4,
    positive_sentiment: 0.2,
    compound_sentiment: -0.2
  }
]

export const mockCategories = [
  { id: 0,
    label: "All",
    href: "/"
  },
  {
    id: 1,
    label: "Technology",
    href: "/?cat=tech"
  },
  {
    id: 2,
    label: "Sports",
    href: "/?cat=sports"
  },
  {
    id: 3,
    label: "Politics",
    href: "/?cat=politics"
  },
  {
    id: 4,
    label: "Entertainment",
    href: "/?cat=entertainment"
  },
  {
    id: 5,
    label: "Finance",
    href: "/?cat=finance"
  },
  {
    id: 6,
    label: "Health",
    href: "/?cat=health"
  },
  {
    id: 7,
    label: "Science",
    href: "/?cat=science"
  },
  {
    id: 8,
    label: "Elections",
    href: "/?cat=elections"
  },
  {
    id: 9,
    label: "Social Media",
    href: "/?cat=socialmedia"
  },
  {
    id: 10,
    label: "Gaming",
    href: "/?cat=gaming"
  },
  {
    id: 11,
    label: "Music",
    href: "/?cat=music"
  },
  {
    id: 12,
    label: "Movies",
    href: "/?cat=movies"
  },
  {
    id: 13,
    label: "TV Shows",
    href: "/?cat=tvshows"
  },
  {
    id: 14,
    label: "Business",
    href: "/?cat=business"
  },
  {
    id: 15,
    label: "Travel",
    href: "/?cat=travel"
  },
  {
    id: 16,
    label: "Food",
    href: "/?cat=food"
  },
  {
    id: 17,
    label: "Fashion",
    href: "/?cat=fashion"
  },
]