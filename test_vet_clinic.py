# UNIT TESTS FOR VET CLINIC SYSTEM
import unittest
from vet_clinic import (
    ClinicDatabase, PetFactory, PetOwner, Appointment,
    VetClinicSystem, Dog, Cat, Bird, Rabbit
)


class TestSingleton(unittest.TestCase):
    """Test the Singleton Pattern"""
    
    def test_singleton_instance(self):
        """Verify only ONE instance of ClinicDatabase exists"""
        db1 = ClinicDatabase()
        db2 = ClinicDatabase()
        self.assertIs(db1, db2, "Database should be the same instance")
        print("✅ Singleton test passed: Only one database instance")


class TestFactory(unittest.TestCase):
    """Test the Factory Pattern"""
    
    def test_create_dog(self):
        pet = PetFactory.create_pet("dog", "PET-001", "Buddy", "OWN-001")
        self.assertIsInstance(pet, Dog)
        self.assertEqual(pet.species, "Dog")
        print("✅ Factory test: Dog created correctly")
    
    def test_create_cat(self):
        pet = PetFactory.create_pet("cat", "PET-002", "Whiskers", "OWN-001")
        self.assertIsInstance(pet, Cat)
        self.assertEqual(pet.species, "Cat")
        print("✅ Factory test: Cat created correctly")
    
    def test_create_bird(self):
        pet = PetFactory.create_pet("bird", "PET-003", "Tweety", "OWN-001")
        self.assertIsInstance(pet, Bird)
        print("✅ Factory test: Bird created correctly")
    
    def test_create_rabbit(self):
        pet = PetFactory.create_pet("rabbit", "PET-004", "Snowball", "OWN-001")
        self.assertIsInstance(pet, Rabbit)
        print("✅ Factory test: Rabbit created correctly")
    
    def test_invalid_pet_type(self):
        with self.assertRaises(ValueError):
            PetFactory.create_pet("dragon", "PET-005", "Spyro", "OWN-001")
        print("✅ Factory test: Invalid pet type raises error")


class TestPetOwner(unittest.TestCase):
    """Test Pet Owner registration"""
    
    def setUp(self):
        # Reset database for each test
        ClinicDatabase._instance = None
        self.system = VetClinicSystem()
    
    def test_register_owner(self):
        owner = self.system.register_owner("Juan Dela Cruz", "09123456789")
        self.assertIsNotNone(owner)
        self.assertEqual(owner.name, "Juan Dela Cruz")
        self.assertEqual(owner.contact, "09123456789")
        self.assertTrue(owner.owner_id.startswith("OWN-"))
        print(f"✅ Owner registration test passed: {owner.owner_id}")
    
    def test_view_owners(self):
        self.system.register_owner("Maria Santos", "09876543210")
        self.assertEqual(len(self.system.db.owners), 1)
        print("✅ View owners test passed")


class TestPetManagement(unittest.TestCase):
    """Test Pet Management"""
    
    def setUp(self):
        ClinicDatabase._instance = None
        self.system = VetClinicSystem()
        self.owner = self.system.register_owner("Juan Dela Cruz", "09123456789")
    
    def test_add_pet(self):
        pet = self.system.add_pet(self.owner.owner_id, "dog", "Buddy")
        self.assertIsNotNone(pet)
        self.assertEqual(pet.name, "Buddy")
        self.assertEqual(pet.species, "Dog")
        print(f"✅ Add pet test passed: {pet.pet_id}")
    
    def test_add_pet_invalid_owner(self):
        pet = self.system.add_pet("OWN-9999", "dog", "Buddy")
        self.assertIsNone(pet)
        print("✅ Invalid owner test passed")


class TestAppointmentManagement(unittest.TestCase):
    """Test Appointment Management"""
    
    def setUp(self):
        ClinicDatabase._instance = None
        self.system = VetClinicSystem()
        self.owner = self.system.register_owner("Juan Dela Cruz", "09123456789")
        self.pet = self.system.add_pet(self.owner.owner_id, "dog", "Buddy")
    
    def test_schedule_appointment(self):
        apt = self.system.schedule_appointment(
            self.pet.pet_id, "2026-09-15", "Vaccination"
        )
        self.assertIsNotNone(apt)
        self.assertEqual(apt.status, "Scheduled")
        self.assertEqual(apt.reason, "Vaccination")
        print(f"✅ Schedule appointment test passed: {apt.appointment_id}")
    
    def test_cancel_appointment(self):
        apt = self.system.schedule_appointment(
            self.pet.pet_id, "2026-09-15", "Vaccination"
        )
        result = self.system.cancel_appointment(apt.appointment_id)
        self.assertTrue(result)
        self.assertEqual(apt.status, "Cancelled")
        print("✅ Cancel appointment test passed")
    
    def test_cancel_nonexistent_appointment(self):
        result = self.system.cancel_appointment("APT-9999")
        self.assertFalse(result)
        print("✅ Cancel nonexistent appointment test passed")
    
    def test_update_appointment_status(self):
        apt = self.system.schedule_appointment(
            self.pet.pet_id, "2026-09-15", "Checkup"
        )
        result = self.system.update_appointment_status(apt.appointment_id, "Completed")
        self.assertTrue(result)
        self.assertEqual(apt.status, "Completed")
        print("✅ Update status test passed")


class TestPetSounds(unittest.TestCase):
    """Test polymorphism - different sounds per pet"""
    
    def test_dog_sound(self):
        dog = Dog("PET-001", "Buddy", "OWN-001")
        self.assertEqual(dog.make_sound(), "Woof! Woof!")
        print("✅ Dog sound test passed")
    
    def test_cat_sound(self):
        cat = Cat("PET-002", "Whiskers", "OWN-001")
        self.assertEqual(cat.make_sound(), "Meow!")
        print("✅ Cat sound test passed")
    
    def test_bird_sound(self):
        bird = Bird("PET-003", "Tweety", "OWN-001")
        self.assertEqual(bird.make_sound(), "Tweet! Tweet!")
        print("✅ Bird sound test passed")
    
    def test_rabbit_sound(self):
        rabbit = Rabbit("PET-004", "Snowball", "OWN-001")
        self.assertEqual(rabbit.make_sound(), "Squeak!")
        print("✅ Rabbit sound test passed")


if __name__ == "__main__":
    print("="*60)
    print("RUNNING UNIT TESTS FOR VET CLINIC SYSTEM")
    print("="*60)
    unittest.main(verbosity=2)