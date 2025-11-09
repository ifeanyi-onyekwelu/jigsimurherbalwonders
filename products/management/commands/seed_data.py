from django.core.management.base import BaseCommand
from django.utils.text import slugify
from products.models import Category, Product
from orders.models import ShippingMethod
from django.contrib.auth.models import User
import random


class Command(BaseCommand):
    help = "Populate the database with sample herbal products data"

    def handle(self, *args, **options):
        self.stdout.write("Creating sample data...")

        # Create categories
        categories_data = [
            {
                "name": "Immune Support",
                "description": "Herbal products to boost and support your immune system naturally.",
            },
            {
                "name": "Digestive Health",
                "description": "Natural remedies for digestive wellness and gut health.",
            },
            {
                "name": "Energy & Vitality",
                "description": "Herbal supplements to increase energy and improve vitality.",
            },
            {
                "name": "Heart Health",
                "description": "Natural products to support cardiovascular health.",
            },
            {
                "name": "Stress Relief",
                "description": "Herbal remedies for stress management and relaxation.",
            },
            {
                "name": "Skin Care",
                "description": "Natural herbal products for healthy and radiant skin.",
            },
        ]

        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data["name"],
                defaults={
                    "slug": slugify(cat_data["name"]),
                    "description": cat_data["description"],
                    "is_active": True,
                },
            )
            categories.append(category)
            if created:
                self.stdout.write(f"Created category: {category.name}")

        # Create products
        products_data = [
            # Immune Support Products
            {
                "name": "Echinacea Immune Booster",
                "category": "Immune Support",
                "price": 24.99,
                "original_price": 29.99,
                "short_description": "Natural immune system support with organic Echinacea extract.",
                "description": "Our premium Echinacea Immune Booster is formulated with the finest organic Echinacea purpurea to naturally support your immune system. This powerful herb has been used for centuries to help the body fight off seasonal challenges and maintain optimal health.",
                "ingredients": "Organic Echinacea purpurea extract (300mg), Vitamin C (60mg), Zinc (10mg), Vegetable cellulose capsule",
                "usage_instructions": "Take 2 capsules daily with meals or as directed by your healthcare professional. Do not exceed recommended dose.",
                "benefits": "Supports immune system function, helps fight seasonal challenges, rich in antioxidants, promotes overall wellness",
                "weight": "60 capsules",
                "stock_quantity": 50,
                "is_featured": True,
            },
            {
                "name": "Elderberry Syrup",
                "category": "Immune Support",
                "price": 19.99,
                "short_description": "Delicious elderberry syrup for immune support.",
                "description": "Made from premium elderberries, this syrup provides natural immune support with a delicious taste that the whole family will love.",
                "ingredients": "Organic elderberries, honey, ginger, cinnamon, cloves",
                "usage_instructions": "Adults: 1-2 tablespoons daily. Children: 1 teaspoon daily.",
                "benefits": "Rich in antioxidants, supports immune function, delicious taste",
                "weight": "8 fl oz",
                "stock_quantity": 30,
            },
            # Digestive Health Products
            {
                "name": "Digestive Enzyme Complex",
                "category": "Digestive Health",
                "price": 32.99,
                "short_description": "Comprehensive digestive enzyme blend for optimal digestion.",
                "description": "This advanced enzyme complex contains a blend of digestive enzymes to help break down proteins, carbohydrates, and fats for better nutrient absorption and digestive comfort.",
                "ingredients": "Protease, Amylase, Lipase, Cellulase, Lactase, Bromelain, Papain",
                "usage_instructions": "Take 1-2 capsules with each meal or as directed by healthcare professional.",
                "benefits": "Supports healthy digestion, reduces bloating, improves nutrient absorption",
                "weight": "90 capsules",
                "stock_quantity": 40,
                "is_featured": True,
            },
            {
                "name": "Ginger Root Extract",
                "category": "Digestive Health",
                "price": 16.99,
                "short_description": "Pure ginger root extract for digestive wellness.",
                "description": "Premium ginger root extract to support healthy digestion and soothe occasional stomach discomfort.",
                "ingredients": "Organic ginger root extract (500mg), vegetable cellulose capsule",
                "usage_instructions": "Take 1 capsule daily with food.",
                "benefits": "Supports digestive health, soothes stomach, natural anti-inflammatory",
                "weight": "60 capsules",
                "stock_quantity": 35,
            },
            # Energy & Vitality Products
            {
                "name": "Ginseng Energy Formula",
                "category": "Energy & Vitality",
                "price": 39.99,
                "original_price": 49.99,
                "short_description": "Premium ginseng blend for natural energy and vitality.",
                "description": "A potent blend of Asian and American ginseng to naturally boost energy levels and support mental clarity without the crash of caffeine.",
                "ingredients": "Asian Ginseng (300mg), American Ginseng (200mg), Rhodiola Rosea (100mg)",
                "usage_instructions": "Take 2 capsules in the morning with breakfast.",
                "benefits": "Natural energy boost, mental clarity, stress adaptation, endurance support",
                "weight": "60 capsules",
                "stock_quantity": 25,
                "is_featured": True,
            },
            {
                "name": "Cordyceps Mushroom Capsules",
                "category": "Energy & Vitality",
                "price": 44.99,
                "short_description": "Premium Cordyceps mushroom for energy and athletic performance.",
                "description": "Wild-harvested Cordyceps sinensis to support energy metabolism and athletic performance naturally.",
                "ingredients": "Organic Cordyceps sinensis mycelium (1000mg), vegetable cellulose capsule",
                "usage_instructions": "Take 2-3 capsules daily, preferably before exercise.",
                "benefits": "Enhances energy, supports athletic performance, improves oxygen utilization",
                "weight": "90 capsules",
                "stock_quantity": 20,
            },
            # Heart Health Products
            {
                "name": "Hawthorn Heart Support",
                "category": "Heart Health",
                "price": 27.99,
                "short_description": "Traditional hawthorn extract for cardiovascular wellness.",
                "description": "Premium hawthorn berry extract traditionally used to support heart health and cardiovascular function.",
                "ingredients": "Organic hawthorn berry extract (500mg), hawthorn leaf extract (200mg)",
                "usage_instructions": "Take 1 capsule twice daily with meals.",
                "benefits": "Supports heart health, promotes healthy circulation, antioxidant protection",
                "weight": "60 capsules",
                "stock_quantity": 30,
            },
            {
                "name": "Omega-3 Fish Oil",
                "category": "Heart Health",
                "price": 34.99,
                "short_description": "High-quality fish oil for heart and brain health.",
                "description": "Pure, molecularly distilled fish oil providing essential omega-3 fatty acids for heart and brain health.",
                "ingredients": "Fish oil concentrate (1000mg), EPA (300mg), DHA (200mg), Vitamin E",
                "usage_instructions": "Take 2 softgels daily with meals.",
                "benefits": "Supports heart health, brain function, healthy inflammation response",
                "weight": "120 softgels",
                "stock_quantity": 45,
            },
            # Stress Relief Products
            {
                "name": "Ashwagandha Stress Relief",
                "category": "Stress Relief",
                "price": 29.99,
                "short_description": "Adaptogenic ashwagandha for stress management.",
                "description": "Premium KSM-66 ashwagandha root extract to help your body adapt to stress and promote calm energy.",
                "ingredients": "KSM-66 Ashwagandha root extract (600mg), black pepper extract (5mg)",
                "usage_instructions": "Take 1-2 capsules daily with or without food.",
                "benefits": "Stress adaptation, promotes calm energy, supports healthy cortisol levels",
                "weight": "60 capsules",
                "stock_quantity": 40,
                "is_featured": True,
            },
            {
                "name": "Chamomile Calm Tea",
                "category": "Stress Relief",
                "price": 12.99,
                "short_description": "Soothing chamomile tea blend for relaxation.",
                "description": "A gentle blend of organic chamomile flowers for natural relaxation and peaceful sleep.",
                "ingredients": "Organic chamomile flowers, organic lemon balm, organic lavender",
                "usage_instructions": "Steep 1 tea bag in hot water for 5-7 minutes. Enjoy 1-2 cups daily.",
                "benefits": "Promotes relaxation, supports restful sleep, caffeine-free",
                "weight": "20 tea bags",
                "stock_quantity": 60,
            },
            # Skin Care Products
            {
                "name": "Turmeric Face Mask",
                "category": "Skin Care",
                "price": 22.99,
                "short_description": "Natural turmeric face mask for radiant skin.",
                "description": "A nourishing face mask with turmeric and botanicals to promote healthy, radiant skin.",
                "ingredients": "Organic turmeric powder, bentonite clay, honey powder, rose petals",
                "usage_instructions": "Mix 1 tablespoon with water to form paste. Apply to clean face, leave 15 minutes, rinse.",
                "benefits": "Brightens skin, reduces inflammation, natural glow",
                "weight": "4 oz powder",
                "stock_quantity": 25,
            },
            {
                "name": "Aloe Vera Healing Gel",
                "category": "Skin Care",
                "price": 14.99,
                "short_description": "Pure aloe vera gel for skin healing and hydration.",
                "description": "99% pure aloe vera gel for soothing and healing irritated or damaged skin.",
                "ingredients": "Organic aloe vera leaf gel (99%), vitamin E, carbomer, phenoxyethanol",
                "usage_instructions": "Apply liberally to affected areas 2-3 times daily or as needed.",
                "benefits": "Soothes irritated skin, promotes healing, intense hydration",
                "weight": "8 oz gel",
                "stock_quantity": 50,
            },
        ]

        # Create products
        for prod_data in products_data:
            category = Category.objects.get(name=prod_data["category"])

            product, created = Product.objects.get_or_create(
                name=prod_data["name"],
                defaults={
                    "slug": slugify(prod_data["name"]),
                    "category": category,
                    "price": prod_data["price"],
                    "original_price": prod_data.get("original_price"),
                    "short_description": prod_data["short_description"],
                    "description": prod_data["description"],
                    "ingredients": prod_data.get("ingredients", ""),
                    "usage_instructions": prod_data.get("usage_instructions", ""),
                    "benefits": prod_data.get("benefits", ""),
                    "weight": prod_data.get("weight", ""),
                    "stock_quantity": prod_data["stock_quantity"],
                    "is_available": True,
                    "is_featured": prod_data.get("is_featured", False),
                },
            )
            if created:
                self.stdout.write(f"Created product: {product.name}")

        # Create shipping methods
        shipping_methods = [
            {
                "name": "Standard Shipping",
                "price": 5.99,
                "estimated_days": 5,
                "description": "Standard ground shipping",
            },
            {
                "name": "Express Shipping",
                "price": 12.99,
                "estimated_days": 2,
                "description": "Express 2-day shipping",
            },
            {
                "name": "Overnight Shipping",
                "price": 24.99,
                "estimated_days": 1,
                "description": "Next business day delivery",
            },
        ]

        for shipping_data in shipping_methods:
            shipping, created = ShippingMethod.objects.get_or_create(
                name=shipping_data["name"], defaults=shipping_data
            )
            if created:
                self.stdout.write(f"Created shipping method: {shipping.name}")

        # Create a superuser if one doesn't exist
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username="admin",
                email="admin@jigsimurherbal.com",
                password="admin123",
                first_name="Admin",
                last_name="User",
            )
            self.stdout.write("Created superuser: admin/admin123")

        self.stdout.write(
            self.style.SUCCESS("Successfully populated database with sample data!")
        )
        self.stdout.write("You can now:")
        self.stdout.write("- Visit the website to see products")
        self.stdout.write("- Login to admin with: admin/admin123")
        self.stdout.write("- Add more products through the admin interface")
