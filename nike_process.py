import time
import scrapy
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
import json


def nike_process(url_target, driver, config):
    driver.get(url_target)
    time.sleep(5)

    driver.execute_script(
        '''window.open("''' +
        url_target +
        '''","_blank");''')

    time.sleep(5)

    new_window_name = driver.window_handles[1]
    driver.close()
    driver.switch_to.window(window_name=new_window_name)

    # Select country
    country = config.country
    country = country.lower()
    try:
        countries_obj = driver.find_elements(By.CLASS_NAME, "nav-bold")

        for cc in range(0, len(countries_obj)):
            if ((country) == str(
                    countries_obj[cc].get_attribute('innerText').lower())):
                print("select and click on ", country)

                # countries_obj[cc].click()
                countries_href_obj = driver.find_elements(
                    By.CLASS_NAME, "hf-language-menu-item")
                countries_href_obj[cc].click()
                time.sleep(3)
                driver.execute_script(
                    '''window.open("''' + url_target + '''","_blank");''')
                time.sleep(3)
                new_window_name = driver.window_handles[1]
                driver.close()
                driver.switch_to.window(window_name=new_window_name)

                break

    except BaseException:
        pass

    # Confirm selection of country
    try:
        cookie_obj = driver.find_elements(
            By.CLASS_NAME, "hf-geomismatch-btn-secondary")
        cookie_obj[0].click()
    except BaseException:
        pass

    # Go in size labels and choose the size that user wanted
    size_obj = driver.find_elements(By.CLASS_NAME, "css-xf3ahq")
    for counter_labels in range(0, len(size_obj)):
        if (size_obj[counter_labels].text == str(config.prefer_product_size)):
            size_obj[counter_labels].click()

    print("size_obj ", size_obj[0].text)

    addtobag_obj = driver.find_elements(By.CLASS_NAME, "add-to-cart-btn")
    addtobag_obj[0].click()

    time.sleep(3)

    driver.get("https://www.nike.com/cart")

    time.sleep(3)

    checkout_button = driver.find_elements(By.CLASS_NAME, "e1udugn30")
    checkout_button[0].click()

    time.sleep(3)

    checkout_guest_button = driver.find_elements(By.CLASS_NAME, "nds-btn")
    checkout_guest_button[5].click()

    time.sleep(3)

    # Start fill the user information and address
    add_address_button = driver.find_elements(By.ID, "addressSuggestionOptOut")
    add_address_button[0].click()

    input_first_name = driver.find_elements(By.ID, "firstName")
    input_first_name[0].send_keys(config.first_name)

    input_last_name = driver.find_elements(By.ID, "lastName")
    input_last_name[0].send_keys(config.last_name)

    input_address = driver.find_elements(By.NAME, "address.address1")
    input_address[0].send_keys(config.address)

    input_city = driver.find_elements(By.NAME, "address.city")
    input_city[0].send_keys(config.city)

    input_state = driver.find_elements(By.NAME, "address.state")
    input_state[0].send_keys(Keys.ENTER)
    state_arr = list(config.state)
    for cc in range(0, len(state_arr)):
        input_state[0].send_keys(state_arr[cc])
        time.sleep(0.5)

    input_state[0].send_keys(Keys.ENTER)

    input_postal_code = driver.find_elements(By.NAME, "address.postalCode")
    input_postal_code[0].send_keys(config.postal_code)

    input_email = driver.find_elements(By.NAME, "address.email")
    input_email[0].send_keys(config.email)

    input_phone = driver.find_elements(By.NAME, "address.phoneNumber")
    input_phone[0].send_keys(config.phone_number)

    save_button = driver.find_elements(By.CLASS_NAME, "btn-md")
    save_button[0].send_keys(Keys.ENTER)

    time.sleep(1)

    try:
        save_button_confirm = driver.find_elements(By.CLASS_NAME, "css-crafp3")
        save_button_confirm[0].send_keys(Keys.ENTER)
    except BaseException:
        pass

    time.sleep(8)

    sel = scrapy.Selector(text=driver.page_source)

    sites = sel.xpath('//title/text()').extract()
    print("title == ", sites)

    cart_summary_subtotal_sel = sel.css("div.ncss-col-sm-4.va-sm-t.ta-sm-r")[0]
    cart_summary_subtotal = cart_summary_subtotal_sel.css("div::text").get()

    cart_summary_estimate_shipping_sel = sel.css(
        "div.ncss-col-sm-3.va-sm-t.ta-sm-r")[0]
    cart_summary_estimate_shipping = cart_summary_estimate_shipping_sel.css(
        "div::text").get()

    cart_summary_estimate_tax_sel = sel.css(
        "div.ncss-col-sm-4.va-sm-t.ta-sm-r")[1]
    cart_summary_estimate_tax = cart_summary_estimate_tax_sel.css(
        "div::text").get()

    cart_summary_delivery_date = sel.css(
        "span.d-sm-b.pl2-sm.css-u55uk5::text")[1].get()

    cart_summary_total_sel = sel.css("div.ncss-col-sm-4.va-sm-t.ta-sm-r")[2]
    cart_summary_total = cart_summary_total_sel.css("div::text").get()

    print("cart_summary_subtotal = ", cart_summary_subtotal)
    print("cart_summary_estimate_shipping = ", cart_summary_estimate_shipping)
    print("cart_summary_estimate_tax = ", cart_summary_estimate_tax)
    print("cart_summary_total = ", cart_summary_total)
    print("cart_summary_delivery_date = ", cart_summary_delivery_date)

    # Collect output in dict then convert to json and save it to csv file
    output_data = {}
    output_data["email"] = config.email
    output_data["subtotal"] = cart_summary_subtotal
    output_data["estimated_shipping"] = cart_summary_estimate_shipping
    output_data["estimated_tax"] = cart_summary_estimate_tax
    output_data["total"] = cart_summary_total
    output_data["estimated_delivery_date"] = cart_summary_delivery_date

    with open(config.output_file, "a") as outfile:
        json.dump(output_data, outfile)
        outfile.write("\n")

    time.sleep(60)
    driver.quit()
