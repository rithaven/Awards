from django.test import TestCase
from django.models import Locations,Image,Review,User,Profile
from django.core.files.Uploadedfile import SimpleUploadedFile


# Create your tests here.
class LocationsTestClass(TestCase):
  
      def setUp(self):
          self.test_location= Location(name='Kanombe')
          self.test_location.save()
      def test_instance(self):
          self.assertTrue(isinstance(self.test_location, Location))

      def test_save_method(self):
          locatations= Location.objects.all()
          self.assertTrue(len(locatations)>0)
      def tearDown(self):
          Location.objects.all().delete()

      def test_delete_location(self):
          self.test_location.delete()
          self.assertEqual(len(Location.objects.all()),0)

class ImageTestClass(TestCase):
      def setUp(self):

          self.kanombe=Location.objects.create(name="kanombe")
  

          self.test_image=Image.objects.create(image='ana.jpeg',name='pop',description='This is a description',location=self.kanombe)
          self.test_image.save()
      def test_save_method(self):
          self.test_image.save()
          test_images= Image.objects.all()
          self.assertTrue(len(test_images)>0)
      def test_save_image(self):
          self.assertEqual(len(Image.objects.all()),1)

      def tearDown(self):
          Image.objects.all().delete()

      def test_delete_image(self):
          Image.delete_image_by_id(self.test_image.id)
          self.assertEqual(len(Image.objects.all()),0)

class Review(TestCase):
      def setUp(self):

          self.delani= User.objects.create(username="ritha")
          self.imge=Image.objects.create(image='image1',user=self.ritha)
          self.comment=Review.objects.create(comment='woooow')
          self.test_review=Review.objects.create(user=self.ritha,image=self.imge,comment='woooow')
          self.test_review.save()
      
      def test_instance(self):
          self.assertTrue(isinstance(self.test_reviews,Review))

      def test_save_method(self):
          reviews= Review.objects.all()
          self.assertTrue(len(reviews)>0)

      def test_save_review(self):
          self.assertEqual(len(Review.objects.all()),1)

      def tearDown(self):
          Review.objects.all().delete()

      def test_delete_review(self):
          self.test_review.delete()
          self.assertEqual(len(Review.objects.all()),0)


