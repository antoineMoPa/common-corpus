#!/usr/bin/env python3
"""Creates the corpus directory structure and all prompts.txt files."""

import os

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "corpus")

# ---------------------------------------------------------------------------
# Stories — grouped by word count
# ---------------------------------------------------------------------------
STORY_GROUPS = {
    "200-400w": {
        "word_target": "200-400",
        "style": "Use very simple words, short sentences, and gentle repetition.",
        "prompts": [
            ("lost_kitten.corpus", "a child who finds a lost kitten and helps it get home"),
            ("red_balloon.corpus", "a child chasing a red balloon through a park"),
            ("bedtime_moon.corpus", "the moon saying goodnight to all the animals"),
            ("muddy_puddles.corpus", "a rainy day spent jumping in muddy puddles"),
            ("hungry_bear.corpus", "a friendly bear looking for honey"),
            ("counting_ducks.corpus", "a child counting ducks at the pond"),
            ("rainbow_colors.corpus", "discovering all the colors of the rainbow"),
            ("baby_bird.corpus", "a baby bird learning to fly for the first time"),
            ("bath_time.corpus", "rubber ducks and bubbles during bath time"),
            ("sharing_toys.corpus", "two friends learning to share their favorite toys"),
        ],
    },
    "400-700w": {
        "word_target": "400-700",
        "style": "Use clear, simple sentences with some descriptive language. Include a lesson or moral.",
        "prompts": [
            ("dragon_friend.corpus", "a child who befriends a small, shy dragon hiding in the garden"),
            ("magic_crayon.corpus", "a crayon whose drawings come to life"),
            ("lost_tooth.corpus", "the adventure of a lost tooth and the tooth fairy"),
            ("treehouse_club.corpus", "friends building a treehouse and solving a disagreement about the rules"),
            ("brave_mouse.corpus", "a tiny mouse who outsmarts a much larger cat"),
            ("garden_helpers.corpus", "insects working together to save a community garden"),
            ("snow_day.corpus", "the unexpected magic of a snow day off from school"),
            ("library_adventure.corpus", "a child who gets pulled into a storybook at the library"),
            ("new_neighbor.corpus", "making friends with a new kid who just moved to the street"),
            ("planet_trip.corpus", "an imaginary rocket ship journey through the solar system"),
        ],
    },
    "700-1200w": {
        "word_target": "700-1200",
        "style": "Use richer vocabulary, longer sentences, and more complex plot structures. Include character development and vivid descriptions.",
        "prompts": [
            ("time_capsule.corpus", "kids who discover a time capsule buried decades ago and try to find its original owners"),
            ("robot_pet.corpus", "a kid who builds a robot pet for a science fair but it starts developing its own personality"),
            ("underground_river.corpus", "exploring a hidden underground river beneath the school"),
            ("code_breaker.corpus", "a mystery involving coded messages left around the neighborhood"),
            ("animal_rescue.corpus", "organizing a rescue mission for animals stranded after a flood"),
            ("haunted_lighthouse.corpus", "investigating strange lights in an old lighthouse, finding a surprising explanation"),
            ("cooking_disaster.corpus", "a cooking competition that goes hilariously wrong but teaches teamwork"),
            ("map_to_nowhere.corpus", "following an old treasure map that leads to something unexpected"),
            ("pen_pal_secret.corpus", "discovering that a mysterious pen pal is closer than expected"),
            ("solar_eclipse.corpus", "a town preparing for a solar eclipse and the strange events around it"),
        ],
    },
    "1200-1800w": {
        "word_target": "1200-1800",
        "style": "Use sophisticated vocabulary, nuanced characters, and layered themes. Explore emotions and ethical dilemmas.",
        "prompts": [
            ("new_school.corpus", "the challenges of starting at a new school mid-year and finding where you belong"),
            ("forest_guardian.corpus", "someone who discovers they can communicate with an ancient forest"),
            ("digital_detox.corpus", "a town where all electronics mysteriously stop working for a week"),
            ("ghost_writer.corpus", "finding an unfinished manuscript in the attic that seems to predict the future"),
            ("bridge_builders.corpus", "two rival groups who must cooperate to build a bridge for their community"),
            ("identity_mirror.corpus", "a mirror that shows not your reflection but who you truly are inside"),
            ("lost_language.corpus", "discovering a forgotten language that unlocks a hidden history of the town"),
            ("storm_chasers.corpus", "a group of friends who track storms and discover something unexpected in the eye of a tornado"),
            ("wrong_accusation.corpus", "being wrongly accused of something and the journey to clear your name"),
            ("parallel_lives.corpus", "two people from very different backgrounds whose lives keep intersecting in surprising ways"),
        ],
    },
    "1800-2500w": {
        "word_target": "1800-2500",
        "style": "Use mature, literary language with complex themes, moral ambiguity, and deep character exploration.",
        "prompts": [
            ("last_summer.corpus", "the last summer before friends scatter to different cities and how they cope with change"),
            ("whistleblower.corpus", "someone who discovers their organization is hiding something and must decide whether to speak up"),
            ("ai_companion.corpus", "forming an unexpected emotional bond with an AI and questioning what connection really means"),
            ("border_town.corpus", "life in a small border town where two cultures meet and sometimes clash"),
            ("memory_market.corpus", "a near-future world where memories can be bought and sold"),
            ("silent_protest.corpus", "organizing a silent protest and confronting the cost of standing up for beliefs"),
            ("inheritance.corpus", "inheriting a grandmother's house and discovering her secret double life"),
            ("ocean_voyage.corpus", "a solo sailing journey that becomes a profound test of self-reliance"),
            ("art_forgery.corpus", "a talented art student drawn into the world of forgery"),
            ("disconnected.corpus", "a week without social media that forces confrontation with real relationships"),
        ],
    },
}

# ---------------------------------------------------------------------------
# Encyclopedia — 8 categories × 20 subcategories
# ---------------------------------------------------------------------------

# For each subcategory we generate 5 articles from different angles:
ARTICLE_ANGLES = [
    ("introduction", "Write a comprehensive encyclopedia article introducing {topic_readable}. Define the subject, explain its significance, and cover its fundamental concepts and principles. Use clear, informative language accessible to a general audience."),
    ("key_concepts", "Write an in-depth encyclopedia article explaining the most important concepts, theories, and principles of {topic_readable}. Provide clear definitions, detailed explanations, and illustrative examples for each concept."),
    ("history", "Write an encyclopedia article tracing the historical development of {topic_readable}. Cover its origins, major milestones, influential figures, and how understanding and practice have evolved over time."),
    ("modern_applications", "Write an encyclopedia article about contemporary applications and current relevance of {topic_readable}. Discuss recent developments, real-world uses, ongoing research, and future prospects."),
    ("beginner_guide", "Write an accessible encyclopedia article that serves as a beginner's guide to {topic_readable}. Use analogies, everyday examples, and clear step-by-step explanations to make the subject approachable for someone with no prior knowledge."),
]

ENCYCLOPEDIA = {
    "science": [
        "physics", "chemistry", "biology", "astronomy", "geology",
        "ecology", "meteorology", "oceanography", "botany", "zoology",
        "genetics", "microbiology", "paleontology", "anatomy", "thermodynamics",
        "optics", "electromagnetism", "quantum-mechanics", "relativity", "materials-science",
    ],
    "history": [
        "ancient-egypt", "ancient-greece", "ancient-rome", "medieval-europe", "renaissance",
        "industrial-revolution", "world-war-1", "world-war-2", "cold-war", "american-revolution",
        "french-revolution", "ottoman-empire", "mongol-empire", "viking-age", "colonial-era",
        "civil-rights-movement", "space-race", "ancient-china", "ancient-india", "mesoamerican-civilizations",
    ],
    "geography": [
        "mountains", "rivers", "deserts", "oceans", "forests",
        "islands", "volcanoes", "glaciers", "plains", "wetlands",
        "caves", "coral-reefs", "tundra", "savannas", "deltas",
        "canyons", "peninsulas", "archipelagos", "plateaus", "fjords",
    ],
    "technology": [
        "computers", "internet", "artificial-intelligence", "robotics", "telecommunications",
        "renewable-energy", "space-technology", "biotechnology", "nanotechnology", "3d-printing",
        "blockchain", "virtual-reality", "autonomous-vehicles", "semiconductors", "satellites",
        "fiber-optics", "drones", "quantum-computing", "cybersecurity", "cloud-computing",
    ],
    "arts": [
        "painting", "sculpture", "architecture", "music-theory", "literature",
        "theater", "dance", "photography", "film", "ceramics",
        "printmaking", "textile-arts", "calligraphy", "mosaic-art", "glassblowing",
        "woodcarving", "metalwork", "animation", "graphic-design", "poetry",
    ],
    "nature": [
        "mammals", "birds", "reptiles", "amphibians", "fish",
        "insects", "arachnids", "marine-life", "trees", "flowers",
        "fungi", "ecosystems", "migration", "symbiosis", "adaptation",
        "photosynthesis", "food-chains", "endangered-species", "biomes", "pollination",
    ],
    "society": [
        "government", "economics", "education", "law", "religion",
        "philosophy", "psychology", "sociology", "anthropology", "linguistics",
        "demographics", "urbanization", "agriculture", "trade", "diplomacy",
        "human-rights", "media", "healthcare", "transportation", "urban-planning",
    ],
    "mathematics": [
        "arithmetic", "algebra", "geometry", "trigonometry", "calculus",
        "statistics", "probability", "number-theory", "set-theory", "logic",
        "combinatorics", "topology", "linear-algebra", "differential-equations", "game-theory",
        "cryptography", "graph-theory", "fractals", "mathematical-modeling", "numerical-analysis",
    ],
}


def slug(name: str) -> str:
    return name.replace("-", "_")


def readable(name: str) -> str:
    return name.replace("-", " ")


def build_story_prompts():
    for group, info in STORY_GROUPS.items():
        dirpath = os.path.join(BASE, "stories", group)
        os.makedirs(dirpath, exist_ok=True)
        lines = []
        for filename, theme in info["prompts"]:
            prompt = (
                f"Write a short story about {theme}. "
                f"{info['style']} "
                f"Aim for {info['word_target']} words."
            )
            lines.append(f"{filename} {prompt}")
        with open(os.path.join(dirpath, "prompts.txt"), "w") as f:
            f.write("\n".join(lines) + "\n")
        print(f"  stories/{group}/prompts.txt ({len(lines)} prompts)")


def build_encyclopedia_prompts():
    for category, subcategories in ENCYCLOPEDIA.items():
        for subcat in subcategories:
            dirpath = os.path.join(BASE, "encyclopedia", category, subcat)
            os.makedirs(dirpath, exist_ok=True)
            topic_readable = f"{readable(subcat)} (in the context of {readable(category)})"
            lines = []
            for angle_slug, angle_template in ARTICLE_ANGLES:
                filename = f"{slug(subcat)}_{angle_slug}.corpus"
                prompt = angle_template.format(topic_readable=topic_readable)
                prompt += " Aim for 800-1200 words."
                lines.append(f"{filename} {prompt}")
            with open(os.path.join(dirpath, "prompts.txt"), "w") as f:
                f.write("\n".join(lines) + "\n")
            print(f"  encyclopedia/{category}/{subcat}/prompts.txt ({len(lines)} prompts)")


def main():
    os.makedirs(BASE, exist_ok=True)
    print("Building story prompts...")
    build_story_prompts()
    print("\nBuilding encyclopedia prompts...")
    build_encyclopedia_prompts()

    # Count totals
    total_dirs = 0
    total_prompts = 0
    for root, dirs, files in os.walk(BASE):
        if "prompts.txt" in files:
            total_dirs += 1
            with open(os.path.join(root, "prompts.txt")) as f:
                total_prompts += sum(1 for line in f if line.strip())
    print(f"\nDone! Created {total_dirs} directories with {total_prompts} total prompts.")


if __name__ == "__main__":
    main()
