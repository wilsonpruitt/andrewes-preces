import Link from "next/link";

// ⚠ This is NOT the printed introduction. Wilson's ruling, 2026-08-31: the
// introduction and preface are authored argument and stay with the book; the
// site gets a short about of its own, which may draw on their material but is
// not them. Do not paste the introduction in here later.
export default function AboutPage() {
  return (
    <div className="apparatus-prose">
      <h1>About this edition</h1>

      <p>
        Lancelot Andrewes (1555&ndash;1626) kept a book of private prayers in his own hand,
        in Greek, Latin and Hebrew. He left it to a friend at his death; it was printed
        after it, and has been edited and reprinted many times since. This is the
        text of the <strong>1853 Parker edition</strong>, which reprints the 1675
        Sheldonian, set beside a new English translation.
      </p>

      <h2>What is here</h2>
      <p>
        The whole volume: Part I&rsquo;s week of daily prayers in Greek with the Latin
        beside it, Part II&rsquo;s <em>Preces Quotidianae</em>, and Part III&rsquo;s
        Creed and penitential prose, printed from MS Harley 6616 and new in 1853. The
        Hebrew stands where the plate sets it.
      </p>
      <p>
        With the text: <Link href="/apparatus">the apparatus</Link> &mdash; 1,676 notes
        anchored to the lines they belong to, and the collation ledgers behind them;{" "}
        <Link href="/scripture">a scripture index</Link> of 2,267 references the 1853
        prints and 94 more it never marks; and <Link href="/synopsis">a synopsis</Link>{" "}
        setting Part III&rsquo;s recension beside the Part II matter it rewrites.
      </p>

      <h2>How to read the parallel</h2>
      <p>
        The columns are keyed by <strong>sense-line</strong>, not by page: line 12 is the
        same line of the same prayer in all three languages, which is what makes the
        parallel honest rather than approximate. Every line carries an anchor, so{" "}
        <code>printed 34, line 27</code> cites identically in this edition and in the
        printed book &mdash; and the printed book&rsquo;s own citations work here.
      </p>
      <p>
        The 1853&rsquo;s references and its errors are kept <em>as printed</em> and
        flagged, never silently mended. Where it cites a psalm by the Vulgate&rsquo;s
        numbering, or the Prayer Book&rsquo;s, or the Authorised Version&rsquo;s &mdash;
        and it does all three, and a hybrid of two &mdash; the figure stands as the plate
        sets it and a note says which it is.
      </p>

      <h2>The Latin</h2>
      <p>
        One caution the printed edition answers in its introduction and this site should
        not leave unsaid: for printed pages 1&ndash;250 the Latin may be an
        editor&rsquo;s rather than Andrewes&rsquo; own. The question is set out at{" "}
        <Link href="/apparatus/latin-question">The Latin Question</Link>, and it is open.
      </p>

      <h2>The book</h2>
      <p>
        There is a printed edition &mdash; the same text and apparatus, set as a Loeb
        with the originals verso and the English recto, and carrying an introduction and
        preface that are not reproduced here. This site is the free home of the English.
      </p>
    </div>
  );
}
