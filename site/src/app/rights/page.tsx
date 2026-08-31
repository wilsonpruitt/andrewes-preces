import Link from "next/link";

export default function RightsPage() {
  return (
    <div className="apparatus-prose">
      <h1>Rights</h1>

      <h2>The source</h2>
      <p>
        The 1853 Parker edition of the <em>Preces Privatae</em>, reprinting the 1675
        Sheldonian, is in the <strong>public domain</strong>. The page images are from
        the University of Toronto&rsquo;s copy, digitised by the Internet Archive.
      </p>

      <h2>The translation and the encoding</h2>
      <p>
        The English translation and the encoding of this edition are &copy; Wroot Press
        and licensed <strong>CC BY&#8209;NC 4.0</strong> &mdash; free to copy, quote and
        adapt for non-commercial use, with attribution.
      </p>
      <p>
        &ldquo;The encoding&rdquo; is not a formality here, and it is worth saying what it
        covers, because it is most of the work: a line-faithful transcription of all three
        scripts, with the plate&rsquo;s indentation and its measured horizontal spacing
        preserved; the sense-line numbering that every citation in this edition depends on;
        1,676 apparatus entries; and a scripture index of 2,361 references, of which 94 are
        identifications the 1853 never marked.
      </p>

      <h2>Where this text lives</h2>
      <p>
        This site is the one published home of the Wroot Press English. Other Wroot Press
        sites link here; none re-hosts it. If you want to point at a passage, the
        line anchors are stable &mdash; <code>/read/1/day1#p34.27</code> is printed page
        34, sense-line 27, and will stay so.
      </p>
      <p>
        <Link href="/about">About this edition</Link>
      </p>
    </div>
  );
}
