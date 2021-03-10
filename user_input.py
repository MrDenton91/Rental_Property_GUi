from tkinter import *
from tkinter import messagebox
from cregs import craigslist_findings, grab_sqft, combined_info
from location_grab import get_citys_in_range
from calculate import dollar_per_sqrt

root =Tk()
root.title('Quality Rental Rates')
root.geometry('1000x600')


def begin():

    #all_url = []

    zip_c = zipcode.get()
    miles_c = miles.get()
    unit = houseing_type.get()
    room =num_rooms.get()
    bath = num_bathrooms.get()
    square_f = square_foot.get()

    if unit == 'Appartment':
        house = False
    elif unit == 'House':
        house = True

    amenities =''
    for pan in amen:
        amenities = amenities + pan.get()
    
    response = messagebox.showinfo('Loading','Please Wait\n Press ok to continue')

    cities_in_range = get_citys_in_range(zip_c,miles_c)

    ## It needs to go through every city that is within in range of the zipcode given,
    ## anything with _f has had duplicates removed.
    list_rent =[]
    list_price = []
    list_sqrt = []
    list_lux = []
    list_house = []

    main_city_rent = []
    main_city_price =[]
    main_city_sqrt = []
    main_city_lux = []
    main_house = []

    for city in cities_in_range[0:-1]:
        all_listings, all_prices = craigslist_findings(city, unit, room, bath, str(amenities))
        main_city_rent.extend(all_listings)
        main_city_price.extend(all_prices)

        all_sqrt, is_luxry = grab_sqft(all_listings, str(amenities),house)
        main_city_sqrt.extend(all_sqrt)
        main_city_lux.extend(is_luxry)
       # main_house.extend(is_house)

    #messagebox.showinfo('Loading','Please Wait\n Grabbing info. \n Press ok to continue')

    for city in cities_in_range:
        all_listings, all_prices = craigslist_findings(city, unit, room, bath, str(amenities))
        list_rent.extend((all_listings))
        list_price.extend((all_prices))

        all_sqrt, is_luxry= grab_sqft(all_listings,str(amenities),house)
        list_sqrt.extend(all_sqrt)
        list_lux.extend(is_luxry)
       # list_house.extend(is_house)

    messagebox.showinfo('Loading','Please Wait\n Calculating info.')

    #### collecting and cleaning information given range
    listing_f, price_f, sqrt_f = combined_info(list_rent, list_price, list_sqrt, list_lux, list_house)
    dper_sqrt_max, dper_avg, dper_min, dper_median = dollar_per_sqrt(price_f, sqrt_f)

    ### Collecting and cleaning information in the city
    city_listing_f, city_price_f, city_sqrt_f = combined_info(main_city_rent, main_city_price, main_city_sqrt, main_city_lux, main_house)
    city_sqrt_max, city_avg, city_min, city_median = dollar_per_sqrt(city_price_f, city_sqrt_f)

    statment = 'For a range of ' + str(miles_c) +' Miles around ' + str(cities_in_range[0]) + '\n\n'
    statment = statment + 'Highest Price per squarefoot is '+ str(round(dper_sqrt_max,2)) + '\n' + 'Average price per squarfoot is '+ str(round(dper_avg, 2)) + '\n'
    statment = statment + 'Median Price per squarefoot is ' + str(round(dper_median,2)) + '\n'
    statment = statment + 'Lowest Price per squarefoot is ' + str(round(dper_min,2)) + '\n\n' 

    if square_f != '' and float(square_f) > 0:
        statment = statment + 'Recommded Price Range: ' + str(round(float(square_f)*dper_median,2)) + ' and ' + str(round(float(square_f)*dper_avg,2)) +'\n\n'

    statment = statment + 'For the city of ' + str(cities_in_range[0]) + '\n\n' + 'Highest Price per squarefoot is '+ str(round(city_sqrt_max,2)) + '\n' + 'Average price per squarfoot is '+ str(round(city_avg, 2)) +'\n'
    statment = statment + 'Median Price per squarefoot is ' + str(round(city_median,2)) + '\n'
    statment = statment + 'Lowest Price per squarefoot is ' + str(round(city_min,2)) +'\n\n'
    if square_f != '' and float(square_f) > 0:
        statment = statment + 'Recommded Price Range: ' + str(round(float(square_f)*city_median,2)) + ' and ' + str(round(float(square_f)*city_avg,2))
    response = messagebox.showinfo('Info.',statment)
    pass


###################################################
Label(root, text='Enter Zipcode for rental: ').grid(row=0,column=0)
zipcode = Entry(root, width=35)
zipcode.grid(row=1,column=0)


###################################################
Label(root, text='How many miles around zipcode: ').grid(row=3,column=0)
miles = Entry(root,width =35)
miles.grid(row=4,column=0)

###################################################
Label(root, text='Enter squarefootage for rental: ').grid(row=6,column=0)
square_foot = Entry(root, width=35)
square_foot.grid(row=7,column=0)


###################################################
houseing_type = StringVar()

Label(root, text='     Select Unit Type:          ').grid(row=0,column=2)
Radiobutton(root, text='Appartment', variable=houseing_type, value='Appartment').grid(row=1,column=2)
Radiobutton(root, text='House', variable=houseing_type, value='House').grid(row=2, column=2)

###################################################
num_rooms = StringVar()
bedroom_list = ['Studio', '1 Bedroom', '2 Bedroom', '3 Bedroom','4+ Bedroom']
Label(root, text='Select number of bedrooms:          ').grid(row=0,column=3)
for key, bed in enumerate(bedroom_list):
    Radiobutton(root, text=bed, variable=num_rooms, value=bed).grid(row=key+1,column=3)



###################################################
num_bathrooms = StringVar()

bathroom_list = ['1 Bathroom','2 Bathrooms','3 Bathrooms','4+ Bathrooms']
Label(root, text='Select number of bathrooms:          ').grid(row=0,column=4)
for key, bathroom in enumerate(bathroom_list):
    Radiobutton(root, text=bathroom, variable=num_bathrooms, value=bathroom).grid(row=key+1,column=4)



###################################################
amen =[]

ammenities_list = ['air conditioning','in unit washer and dryer','washer and dryer hoockups','dishwasher','wheelchair access',
                'parking','laundry facilities','fitness center','pool','elevator','dog friendly','cat friendly', 'luxury',
                'furnished','utilities included', 'modern', 'renovated', 'granite counter tops', 'updated kitchen', 'view', 'patio', 'balcony']

for i in range(len(ammenities_list)):
    amen.append(StringVar())
Label(root, text='Select Ammenities:').grid(row=0,column=5)
for key, ammenities in enumerate(ammenities_list):

    Checkbutton(root, text= ammenities, variable=amen[key], onvalue=ammenities +', ', offvalue='').grid(row=key+1,column=5)
    
############################################################################

submit_btn = Button(root, text='Search', command=begin).grid(row =9, column=0)

############################################################################




mainloop()