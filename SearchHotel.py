# Search Hotel is an application where user can search hotel with some filters
# here are STEPS to make it.
# in MODELS.PY
class Emenities(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Hotel(models.Model):
    hotel_name = models.CharField(max_length=30)
    hotel_desc = models.TextField()
    hotel_img = models.CharField(max_length=500)
    price = models.IntegerField()
    emenities = models.ManyToManyField(Emenities) # this is many to many field because one hotel can have many emenities
    
    def __str__(self):
        return self.hotel_name
 
# Add Models to Admin.py
admin.site.register(Emenities)
admin.site.register(Hotel)

# Create Views (here we created out own API without any third party tool)
def home(request):
    emenities = Emenities.objects.all()
    context = {
        'emenities':emenities
    }
    return render(request,'home.html',context)

def api_hotels(request): #API without any third party library
    hotels_obj = Hotel.objects.all()

    price = request.GET.get('price')
    if price:
        hotels_obj = hotels_obj.filter(price__lte = price)
    else:
        pass

    emenities = request.GET.get('emenities')
    if emenities:
        emenities = emenities.split(",")
        em = []
        for e in emenities:
            try:
                em.append(int(e))
            except Exception as e:
                pass
        hotels_obj = hotels_obj.filter(emenities__in = em).distinct()

    payload = []
    for hotel in hotels_obj:
        result = {}
        result['hotel_name'] = hotel.hotel_name
        result['hotel_desc'] = hotel.hotel_desc
        result['hotel_img'] = hotel.hotel_img
        result['hotel_price'] = hotel.price
        payload.append(result)
    return JsonResponse(payload,safe=False)
  
  
