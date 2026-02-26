from farm import Farm, create_initial_animals, Cow, Chicken, generate_unique_id


def print_animal_counts(farm: Farm, title: str = ""):
    counts = farm.get_animal_count()
    print(f"\n{'='*50}")
    print(f"Животные на ферме {title}")
    print(f"{'='*50}")
    print(f"🐮 Коров: {counts.get('cow', 0)}")
    print(f"🐔 Кур: {counts.get('chicken', 0)}")


def simulate_week(farm: Farm, week_num: int):
    print(f"\n📅 Неделя {week_num}")
    print("-" * 30)
    
    weekly = {}
    for day in range(1, 8):
        daily = farm.collect_products()
        for product, amount in daily.items():
            weekly[product] = weekly.get(product, 0) + amount
        
        desc = []
        if "milk" in daily:
            desc.append(f"🥛 {daily['milk']}л молока")
        if "eggs" in daily:
            desc.append(f"🥚 {daily['eggs']} яиц")
        print(f"  День {day}: {', '.join(desc)}")
    
    print(f"\n📊 ИТОГО за неделю:")
    if "milk" in weekly:
        print(f"  🥛 Молоко: {weekly['milk']} литров")
    if "eggs" in weekly:
        print(f"  🥚 Яйца: {weekly['eggs']} штук")


def main():
    print("🌾 СИМУЛЯТОР ФЕРМЫ")
    
    farm = Farm()
    farm.add_animals(create_initial_animals())
    
    print_animal_counts(farm, "(неделя 1)")
    simulate_week(farm, 1)
    
    print("\n🛒 Покупаем новых животных...")
    counts = farm.get_animal_count()
    cow_count = counts.get("cow", 0)
    chicken_count = counts.get("chicken", 0)
    
    farm.add_animal(Cow(generate_unique_id("cow", cow_count + 1)))
    for i in range(5):
        farm.add_animal(Chicken(generate_unique_id("chicken", chicken_count + i + 1)))
    
    print_animal_counts(farm, "(после покупки)")
    simulate_week(farm, 2)
    
    print("\n✨ Симуляция завершена!")


if __name__ == "__main__":
    main()