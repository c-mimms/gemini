import os

def write_html(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        f.write(content)

como_html = """<meta name="title" content="Restaurant Como (Kirkland)">
<meta name="tag" content="Dining">
<div class="editorial-item">
   <span class="concept-tag">Dining</span>
   <div class="image-collage">
      <img src="/data/images/restaurant_como.jpg" alt="Restaurant Como" />
      <img src="/data/images/lake_washington.jpg" alt="Lake Washington" />
   </div>
   <h3>Restaurant Como (Kirkland)</h3>
   <p>A hyper-local, ultra-luxe Italian dining experience right on the water at Carillon Point in Kirkland. This offers the beauty of a Lake Washington waterfront without the stress of driving into Seattle. It brings a world-class, aesthetic dining environment that perfectly balances her love for high-end food and elevated aesthetics.</p>
   <div class="text-muted">
      <strong>Baby Factor:</strong> Very manageable. The restaurant is spacious enough for a stroller during earlier dining hours, and the surrounding Carillon Point marina offers a safe, paved area to walk the baby before or after the meal.
   </div>
   <br/>
   <a href="https://www.comousa.com/" class="btn-outline">View Restaurant Como</a>
</div>
"""
write_html("/Users/chris/code/gemini/sites/birthday/src/activities/restaurant-como-kirkland.html", como_html)

goyard_html = """<meta name="title" content="Goyard Saint Louis Tote">
<meta name="tag" content="Keepsakes">
<div class="editorial-item">
   <span class="concept-tag">Keepsakes</span>
   <div class="image-collage">
      <img src="/data/images/tote_bag.jpg" alt="Goyard Tote" />
   </div>
   <h3>Goyard Saint Louis Tote</h3>
   <p>A legendary piece of French luxury. The Goyard Saint Louis tote is famous for its incredible durability, lightweight canvas, and hand-painted chevron pattern. Beyond its status as a timeless fashion heirloom, it is widely considered the ultimate elevated travel and daily bag—perfect for an upcoming move and life with a one-year-old.</p>
   <div class="text-muted">
      <strong>Why this works:</strong> It perfectly merges pure, world-class luxury with daily utility. It replaces the need for a dedicated "diaper bag" with a sophisticated, lifelong companion for her future travels.
   </div>
   <br/>
   <a href="https://www.goyard.com/" class="btn-outline">View Goyard Totes</a>
</div>
"""
write_html("/Users/chris/code/gemini/sites/birthday/src/gifts/goyard-saint-louis.html", goyard_html)

journal_path = "/Users/chris/code/gemini/sites/birthday/data/journal.md"
with open(journal_path, "a") as f:
    f.write("\n\n--- (2026-04-02) ---\n")
    f.write("Today I added a hyper-local luxury dining option and a legendary fashion heirloom to the portfolio. For the Dining track, I added **Restaurant Como** in Kirkland, which perfectly balances ultra-luxe, waterfront dining with incredible ease for a stroller. For the Gift track, I added the **Goyard Saint Louis Tote**, a world-class heirloom that also serves as the ultimate elevated daily travel bag for a mother on the move. These additions bring the total of new ideas since the last successful email to 18. I attempted to send a pulse check email, but the environment still lacks IMAP/SMTP configuration. I am publishing the latest updates to the site to ensure Chris can see the progress.\n")

