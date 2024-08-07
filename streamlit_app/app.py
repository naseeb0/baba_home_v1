import streamlit as st
import requests

st.title("PreConstruction Upload Form")

# Form fields
with st.form(key='preconstruction_form', clear_on_submit=True):
    meta_title = st.text_input("Meta Title")
    meta_description = st.text_input("Meta Description")
    project_name = st.text_input("Project Name")
    slug = st.text_input("Slug")
    storeys = st.text_input("Storeys")
    total_units = st.text_input("Total Units")
    price_starts = st.number_input("Price Starts", min_value=0.0, format="%.2f")
    price_end = st.number_input("Price End", min_value=0.0, format="%.2f")
    description = st.text_area("Description")
    project_address = st.text_input("Project Address")
    postal_code = st.text_input("Postal Code")
    latitude = st.text_input("Latitude")
    longitude = st.text_input("Longitude")
    occupancy = st.text_input("Occupancy")
    status = st.selectbox("Status", ["Upcoming", "Selling", "Planning Phase", "Sold out"])
    project_type = st.selectbox("Project Type", ["Condo", "Townhome", "Semi-Detached", "Detached", "NaN"])
    street_map = st.text_area("Street Map")
    developer_name = st.text_input("Developer Name")
    developer_website = st.text_input("Developer Website")
    developer_details = st.text_area("Developer Details")
    developer_slug = st.text_input("Developer Slug")
    city_name = st.text_input("City Name")
    city_lat = st.text_input("City Latitude")
    city_long = st.text_input("City Longitude")
    city_details = st.text_area("City Details")
    image_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

    submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        if image_file is not None:
            files = {'images': image_file.getvalue()}
            data = {
                'meta_title': meta_title,
                'meta_description': meta_description,
                'project_name': project_name,
                'slug': slug,
                'storeys': storeys,
                'total_units': total_units,
                'price_starts': price_starts,
                'price_end': price_end,
                'description': description,
                'project_address': project_address,
                'postal_code': postal_code,
                'latitude': latitude,
                'longitude': longitude,
                'occupancy': occupancy,
                'status': status,
                'project_type': project_type,
                'street_map': street_map,
                'developer[name]': developer_name,
                'developer[website]': developer_website,
                'developer[details]': developer_details,
                'developer[slug]': developer_slug,
                'city[name]': city_name,
                'city[city_lat]': city_lat,
                'city[city_long]': city_long,
                'city[city_details]': city_details,
            }

            response = requests.post('http://localhost:8000/api/preconstruction/', data=data, files=files)

            if response.status_code == 201:
                st.success("PreConstruction data submitted successfully!")
            else:
                st.error(f"Error: {response.text}")
        else:
            st.error("Please upload an image.")
