# Weed Spread Homework
# Navid Nafiuzzaman, Vincent Li, Karl Coelho


from flask import Flask			# Making the connecting data across the web.
from flask import render_template	# How to render a FLASK template to HTML.
from flask import request		# How the data requests a GUI setting.

import random


app = Flask( __name__ )


#   ##########################################################################
#
#  Student code will go here...
#

def age_infested(yard_age):
    for square_index in range(len(yard_age)):
        if yard_age[square_index] > 0:
            yard_age[square_index] += 1

def ruin_old_infested(yard, yard_age):
    for square_index in range(len(yard)):
        if yard[square_index] == 1 and yard_age[square_index] > 14:
            yard[square_index] = 2

def gen_weed_spread(reproduction_rate, cross_contamination_rate):
    yard = [0] * 100000
    yard_age = [0] * 100000
    weeds = 10
    suspectible = len(yard) - weeds

    for i in range(weeds):
        r = random.randint(0, len(yard)/2)
        yard_age[r] = 1
        yard[r] = 1

    day = 0
    day_cases = []
    while yard.count(1) != 0 or yard.count(2) != len(yard):
        i_to = reproduction_rate * min(yard.count(1) * cross_contamination_rate, yard.count(0))
        new_exposures = min(yard.count(1) * cross_contamination_rate, yard.count(0))

        infested = 0
        sus = 0

        for _ in range(round(new_exposures)):
            r = random.uniform(0,1)

            if r > reproduction_rate:
                infested += 1
            else:
                sus += 1

        day_count = 0
        for _ in range(infested):
            day_count += 1

            r = random.randint(0, len(yard)-1)
            
            while(yard[r] != 0):
                r = random.randint(0, len(yard)-1)

            yard_age[r] = 1
            yard[r] = 1

        day_cases.append(day_count)
        ruin_old_infested(yard, yard_age)
        age_infested(yard_age)
        day += 1

    return day_cases

def sim_weed_spread(r,k):
    #  This is the main work-engine of the simulation.
    #     #  r = fundamental reproduction rate of the weeds.
    #     #  k = how much cross-contamination happens in the yard.
    n_days           = 365 * 2;
    weed_infected    = np.empty( (n_days,1) );
    weed_infected[:] = np.nan;	# Set entire array to the sentinal value NaN.

    # How many days to run the simulation for...
 
    N_DAYS_OF_CRUD   = 12
    for idx in range(0, N_DAYS_OF_CRUD ) :
        weed_infected[idx] = r * idx;

    # Create a new array (i.e. a list) :
    the_answer = list(weed_infected[~ np.isnan(weed_infected) ])

    return the_answer


# ##############################################################################
#
#  This is a pure python computation that is done here.
#
#  Y is the slider value.  It is initally zero, but later on it is called 
#  with the new slider value.
#
def create_line_data(y=0):
    # This method does the actual calculation for simulating Weed spread
    #
    # This is a list comprehension:  This a "for loop" written by Yoda.
    # new_values = [original_value + y           for original_value in values]

    fractn 		=  float(y)
    # weed_count_per_day  =  sim_weed_spread(fractn,4.3)	# Folks meet 4.3 people...
    weed_count_per_day = gen_weed_spread(fractn, 1.0)
    print("weed_count_per_day = ", weed_count_per_day )

    # Two ways of creating variable length lists:
    x_labels    = list(  range(0,len(weed_count_per_day) ) )

    return x_labels, weed_count_per_day


# ##############################################################################
#
#  This runs the FLASK route, and we will find this in 127.0.0.1:5000
#
#  You must have this URL be consistent.
#
@app.route("/my_page_name") 		# <-- TELLS WHICH SUB-FOLDER TO PUT THIS ON, on the LOCAL INTERNET
def home():
    # 
    #  The main driving function which renders the my_first_flask_page.html template.
    #
    #  Generates the x and y axes, coordinates and passes them to the chart.js 
    #  method in the index.html file.
    #  :return: renders first page of the application.
    #  
    #  This does the setup of the original form.  
    #
    y = 0.2

    # Create the original data to render.
    # This gives the original values to plot.
    x_labels, new_values = create_line_data(y)


    #
    # render_template is a built-in FLASK routine.
    # NOTE:  DO NOT USE INDEX.HTML!! 
    #
    # This renders the template file, "my_first_flast_page.html".
    # AND it passes in two parameters:
    #   1.  values, (previously computed).
    #   2.  new_values (y-axis).
    return render_template("my_first_flask_page.html", values=x_labels, newValues=new_values, y=y)



#
#  This is a callback function which is called when the "submit" function changes.
#
#  / is the root in the HTML file.
#  If you change this to use '/home' is the root in the HTML file.
#
#  This must agree with the corresponding *.html file.
#
@app.route("/my_page_name", methods=['POST', 'GET'])
def background_process():
    """
    This method is used to catch the value of sliders from the web page and generate the new graph based on those values.
    :return: renders the updated graph
    """

    #  Go get the value of the slider bar that is called "y_slider"
    y = request.form["y_slider"]

    #  Based on that new slider value, then
    #  recreate the new graph values.
    x_labels, new_values = create_line_data( y )

    #  Actually graph the new values:
    #
    #  The page will be refreshed. In order to keep the slider bar the same 
    #  (so that it looks like the user's actions took effect) you need to 
    #  explicitly set the slider bar back to where it was.
    #
    #  There are other ways to do this, but this way works.
    #
    return render_template("my_first_flask_page.html", values=x_labels, newValues=new_values, y=y)


# ##############################################################################
#
#  Trigger the main routine.
#
#  This calls the HOME() method first, and renders index.html
#
if __name__ == "__main__":
    print('#')
    print('#')
    print('#  Entry point is at /my_page_name on the specified port.')
    print('#  In the browser, open')
    print('#                   http://127.0.0.1:5000/my_page_name  ')
    print('#')
    print('#')
    app.run(debug=True)

