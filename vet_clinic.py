# VET CLINIC APPOINTMENT MANAGEMENT SYSTEM
# With Singleton and Factory Design Patterns

import random
from datetime import datetime


# ============================================
# SINGLETON PATTERN - Clinic Database
# ============================================

class ClinicDatabase:
    """Singleton class - only ONE instance can exist"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.owners = []
            cls._instance.pets = []
            cls._instance.appointments = []
            cls._instance.owner_counter = 1001
            cls._instance.pet_counter = 2001
            cls._instance.appointment_counter = 3001
        return cls._instance
    
    def generate_owner_id(self):
        oid = f"OWN-{self.owner_counter}"
        self.owner_counter += 1
        return oid
    
    def generate_pet_id(self):
        pid = f"PET-{self.pet_counter}"
        self.pet_counter += 1
        return pid
    
    def generate_appointment_id(self):
        aid = f"APT-{self.appointment_counter}"
        self.appointment_counter += 1
        return aid


# ============================================
# FACTORY PATTERN - Pet Creation
# ============================================

class Pet:
    """Base Pet class"""
    def __init__(self, pet_id, name, owner_id, species):
        self.pet_id = pet_id
        self.name = name
        self.owner_id = owner_id
        self.species = species
    
    def get_info(self):
        return f"ID: {self.pet_id} | {self.name} ({self.species}) | Owner: {self.owner_id}"
    
    def make_sound(self):
        return "..."


class Dog(Pet):
    def __init__(self, pet_id, name, owner_id):
        super().__init__(pet_id, name, owner_id, "Dog")
    
    def make_sound(self):
        return "Woof! Woof!"


class Cat(Pet):
    def __init__(self, pet_id, name, owner_id):
        super().__init__(pet_id, name, owner_id, "Cat")
    
    def make_sound(self):
        return "Meow!"


class Bird(Pet):
    def __init__(self, pet_id, name, owner_id):
        super().__init__(pet_id, name, owner_id, "Bird")
    
    def make_sound(self):
        return "Tweet! Tweet!"


class Rabbit(Pet):
    def __init__(self, pet_id, name, owner_id):
        super().__init__(pet_id, name, owner_id, "Rabbit")
    
    def make_sound(self):
        return "Squeak!"


class PetFactory:
    """Factory class - creates different pet types"""
    @staticmethod
    def create_pet(pet_type, pet_id, name, owner_id):
        pet_type = pet_type.lower()
        
        if pet_type == "dog":
            return Dog(pet_id, name, owner_id)
        elif pet_type == "cat":
            return Cat(pet_id, name, owner_id)
        elif pet_type == "bird":
            return Bird(pet_id, name, owner_id)
        elif pet_type == "rabbit":
            return Rabbit(pet_id, name, owner_id)
        else:
            raise ValueError(f"Unknown pet type: {pet_type}")


# ============================================
# PET OWNER MANAGEMENT
# ============================================

class PetOwner:
    def __init__(self, owner_id, name, contact):
        self.owner_id = owner_id
        self.name = name
        self.contact = contact
    
    def get_info(self):
        return f"ID: {self.owner_id} | Name: {self.name} | Contact: {self.contact}"


# ============================================
# APPOINTMENT MANAGEMENT
# ============================================

class Appointment:
    def __init__(self, appointment_id, pet_id, date, reason):
        self.appointment_id = appointment_id
        self.pet_id = pet_id
        self.date = date
        self.reason = reason
        self.status = "Scheduled"
    
    def get_info(self):
        return f"ID: {self.appointment_id} | Pet: {self.pet_id} | Date: {self.date} | Reason: {self.reason} | Status: {self.status}"


# ============================================
# MAIN SYSTEM
# ============================================

class VetClinicSystem:
    def __init__(self):
        self.db = ClinicDatabase()  # Singleton
    
    # Owner methods
    def register_owner(self, name, contact):
        owner_id = self.db.generate_owner_id()
        owner = PetOwner(owner_id, name, contact)
        self.db.owners.append(owner)
        print(f"\n✅ Owner registered! ID: {owner_id}")
        return owner
    
    def view_owners(self):
        if not self.db.owners:
            print("No owners registered.")
            return
        print("\n" + "="*60)
        print("PET OWNERS")
        print("="*60)
        for o in self.db.owners:
            print(o.get_info())
    
    # Pet methods
    def add_pet(self, owner_id, pet_type, pet_name):
        # Find owner
        owner = None
        for o in self.db.owners:
            if o.owner_id == owner_id:
                owner = o
                break
        
        if not owner:
            print(f"❌ Owner {owner_id} not found!")
            return None
        
        pet_id = self.db.generate_pet_id()
        try:
            pet = PetFactory.create_pet(pet_type, pet_id, pet_name, owner_id)
            self.db.pets.append(pet)
            print(f"\n✅ {pet_type} added! ID: {pet_id}")
            print(f"   Sound: {pet.make_sound()}")
            return pet
        except ValueError as e:
            print(f"❌ {e}")
            return None
    
    def view_pets(self):
        if not self.db.pets:
            print("No pets registered.")
            return
        print("\n" + "="*60)
        print("PETS")
        print("="*60)
        for p in self.db.pets:
            print(p.get_info())
    
    # Appointment methods
    def schedule_appointment(self, pet_id, date, reason):
        # Check if pet exists
        pet = None
        for p in self.db.pets:
            if p.pet_id == pet_id:
                pet = p
                break
        
        if not pet:
            print(f"❌ Pet {pet_id} not found!")
            return None
        
        appointment_id = self.db.generate_appointment_id()
        appointment = Appointment(appointment_id, pet_id, date, reason)
        self.db.appointments.append(appointment)
        print(f"\n✅ Appointment scheduled! ID: {appointment_id}")
        return appointment
    
    def view_appointments(self):
        if not self.db.appointments:
            print("No appointments scheduled.")
            return
        print("\n" + "="*60)
        print("APPOINTMENTS")
        print("="*60)
        for a in self.db.appointments:
            print(a.get_info())
    
    def cancel_appointment(self, appointment_id):
        for a in self.db.appointments:
            if a.appointment_id == appointment_id:
                if a.status == "Cancelled":
                    print(f"❌ Appointment {appointment_id} is already cancelled.")
                    return False
                a.status = "Cancelled"
                print(f"\n✅ Appointment {appointment_id} cancelled.")
                return True
        print(f"❌ Appointment {appointment_id} not found!")
        return False
    
    def update_appointment_status(self, appointment_id, status):
        valid = ["Scheduled", "Completed", "Cancelled"]
        for a in self.db.appointments:
            if a.appointment_id == appointment_id:
                if status in valid:
                    a.status = status
                    print(f"\n✅ Appointment {appointment_id} status: {status}")
                    return True
                else:
                    print(f"❌ Invalid status. Use: {valid}")
                    return False
        print(f"❌ Appointment {appointment_id} not found!")
        return False


# ============================================
# MAIN MENU
# ============================================

def main_menu():
    system = VetClinicSystem()
    
    while True:
        print("\n" + "="*60)
        print("🐾 PAWS AND CARE VET CLINIC")
        print("="*60)
        print("1. Register Pet Owner")
        print("2. View Pet Owners")
        print("3. Add Pet")
        print("4. View Pets")
        print("5. Schedule Appointment")
        print("6. View Appointments")
        print("7. Cancel Appointment")
        print("8. Update Appointment Status")
        print("9. Exit")
        print("="*60)
        
        choice = input("Enter choice (1-9): ").strip()
        
        if choice == '1':
            name = input("Owner name: ").strip()
            contact = input("Contact number: ").strip()
            system.register_owner(name, contact)
        
        elif choice == '2':
            system.view_owners()
        
        elif choice == '3':
            system.view_owners()
            owner_id = input("Enter Owner ID: ").strip()
            print("\nPet types: dog, cat, bird, rabbit")
            pet_type = input("Enter pet type: ").strip()
            pet_name = input("Enter pet name: ").strip()
            system.add_pet(owner_id, pet_type, pet_name)
        
        elif choice == '4':
            system.view_pets()
        
        elif choice == '5':
            system.view_pets()
            pet_id = input("Enter Pet ID: ").strip()
            date = input("Enter date (YYYY-MM-DD): ").strip()
            reason = input("Enter reason: ").strip()
            system.schedule_appointment(pet_id, date, reason)
        
        elif choice == '6':
            system.view_appointments()
        
        elif choice == '7':
            system.view_appointments()
            apt_id = input("Enter Appointment ID to cancel: ").strip()
            system.cancel_appointment(apt_id)
        
        elif choice == '8':
            system.view_appointments()
            apt_id = input("Enter Appointment ID: ").strip()
            status = input("New status (Scheduled/Completed/Cancelled): ").strip()
            system.update_appointment_status(apt_id, status)
        
        elif choice == '9':
            print("\n👋 Thank you for using Paws and Care Vet Clinic System!")
            break
        
        else:
            print("❌ Invalid choice.")


if __name__ == "__main__":
    main_menu()