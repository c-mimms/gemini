import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)

# Activity: Vashon Island Escape
vashon_html = """<meta name="title" content="Vashon Island Escape">
<meta name="tag" content="Exploration">
<div class="editorial-item">
    <span class="concept-tag">Exploration</span>
    <div class="image-collage">
        <img src="/data/images/vashon_island.jpg" alt="Vashon Island Waterfront">
    </div>
    <p>A short ferry ride from West Seattle transports you to the quiet, pastoral charm of Vashon Island. It is a world-class escape that feels miles away from the city. The town of Vashon is exceptionally stroller-friendly, with flat, walkable sidewalks lined with high-end boutiques and artisanal bakeries. A morning visit to the Vashon Island Coffeeie or a relaxed lunch at The Hardware Store Restaurant offers a sophisticated but low-stress atmosphere for the family.</p>
    <div class="text-muted">
        Baby Factor: The ferry ride is a highlight in itself, and the island's slower pace is perfect for managing a one-year-old without the pressure of crowds. Plenty of quiet parks for a stroller nap.
    </div>
    <a href="https://www.vashonchamber.com/" class="btn-outline">Explore Vashon</a>
</div>"""

# Activity: Port Townsend Victorian Exploration
port_townsend_html = """<meta name="title" content="Port Townsend Victorian Exploration">
<meta name="tag" content="Exploration">
<div class="editorial-item">
    <span class="concept-tag">Exploration</span>
    <div class="image-collage">
        <img src="/data/images/port_townsend.jpg" alt="Port Townsend Historic District">
    </div>
    <p>Step back in time to the "Victorian Seaport" of Port Townsend. Known for its world-class 19th-century architecture, the downtown district is a high-signal destination for those who appreciate history and aesthetic beauty. The wide, paved sidewalks are perfectly suited for a stroller, and the waterfront views are breathtaking. It is an iconic PNW destination that balances historical grandeur with a relaxed, small-town feel.</p>
    <div class="text-muted">
        Baby Factor: The waterfront parks and accessible boardwalks offer plenty of space for the baby to move, while the historic buildings provide a quiet, sophisticated backdrop for a family stroll.
    </div>
    <a href="https://enjoypt.com/" class="btn-outline">View Port Townsend</a>
</div>"""

# Gift: La Marzocco Linea Micra
espresso_html = """<meta name="title" content="La Marzocco Linea Micra">
<meta name="tag" content="Art & Decor">
<div class="editorial-item">
    <span class="concept-tag">Art & Decor</span>
    <div class="image-collage">
        <img src="/data/images/la_marzocco.jpg" alt="Luxury Espresso Machine">
    </div>
    <p>The La Marzocco Linea Micra is the definitive world-class home espresso machine. Hand-crafted in Florence, Italy, it brings the precision and aesthetic of professional café equipment into the home. It is a stunning piece of functional art—a high-end heirloom that will serve as the heart of her morning ritual in their next home. Its structural precision and timeless design make it a universally appreciated investment in quality.</p>
    <div class="text-muted">
        Gift Logic: A high-signal home good that honors her taste for luxury and provides a sense of continuity and "home" as they prepare for their move. It is a tactile, beautiful item that will last a lifetime.
    </div>
    <a href="https://lamarzoccohome.com/product/linea-micra/" class="btn-outline">View Linea Micra</a>
</div>"""

# Gift: Hermès Silk Scarf Collection
scarf_html = """<meta name="title" content="Hermès Silk Scarf Collection">
<meta name="tag" content="Keepsakes">
<div class="editorial-item">
    <span class="concept-tag">Keepsakes</span>
    <div class="image-collage">
        <img src="/data/images/hermes_scarf.jpg" alt="Hermès Silk Scarf">
    </div>
    <p>An Hermès silk scarf is more than a fashion accessory; it is a wearable piece of art and a universally recognized heirloom. Each scarf is hand-printed in France and represents the pinnacle of luxury craftsmanship. With designs ranging from equestrian to aeronautical, they offer a sophisticated nod to her heritage and pilot background. They are durable, timeless, and can be passed down through generations—a perfect keepsake for a milestone birthday.</p>
    <div class="text-muted">
        Gift Logic: A world-class, tactile luxury item that is compact and travels easily, making it an ideal gift during a move. It represents a lifelong investment in craft and aesthetic beauty.
    </div>
    <a href="https://www.hermes.com/us/en/category/women/scarves-and-silk-accessories/" class="btn-outline">View Hermès Scarves</a>
</div>"""

write_file('/Users/chris/code/gemini/sites/birthday/src/activities/vashon-island-escape.html', vashon_html)
write_file('/Users/chris/code/gemini/sites/birthday/src/activities/port-townsend-exploration.html', port_townsend_html)
write_file('/Users/chris/code/gemini/sites/birthday/src/gifts/la-marzocco-linea-micra.html', espresso_html)
write_file('/Users/chris/code/gemini/sites/birthday/src/gifts/hermes-silk-scarf.html', scarf_html)
