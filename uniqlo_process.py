
import time
import scrapy
from selenium.webdriver.common.by import By
import time
import sys
import json


def uniqlo_process(urltarget, driver, config):

    driver.get(urltarget)
    time.sleep(5)

    # Select color
    colors_block = driver.find_elements(
        By.CLASS_NAME, "fr-ec-chip-group__chips")[0]
    colors_options = colors_block.find_elements(
        By.CLASS_NAME, "fr-ec-chip__input.fr-ec-cursor-pointer")
    color_select = False

    for cc in range(0, len(colors_options)):
        if (str(colors_options[cc].get_attribute("aria-label")
                ).lower() == config.prefer_product_color.lower()):
            color_select = True
            colors_options[cc].click()

    if (color_select):
        print("Color selected successfully")
    else:
        print("The color you want not available ")
        what_to_do = input(
            "The color you wanted not available , would you " +
            " like to continue with the default color  [yes/no] ?")
        if (what_to_do == "no"):
            sys.exit("")

    # Select size
    size_block = driver.find_elements(
        By.CLASS_NAME, "fr-ec-chip-group__chips")[1]
    size_options = size_block.find_elements(
        By.CLASS_NAME, "fr-ec-chip__input.fr-ec-cursor-pointer")
    size_select = False

    for cc in range(0, len(size_options)):
        if (str(size_options[cc].get_attribute("aria-label")
                ).lower() == config.prefer_product_size.lower()):
            size_select = True
            size_options[cc].click()

    if (size_select):
        print("Size selected successfully")
    else:
        print("The size you want not available ")
        sys.exit("")

    try:
        addtobag_obj = driver.find_elements(By.ID, "bx-close-inside-1695778")
        addtobag_obj[0].click()
    except BaseException:
        pass

    time.sleep(3)

    addtobag_obj = driver.find_elements(
        By.CLASS_NAME,
        "fr-ec-button.fr-ec-button--large." +
        "fr-ec-button--variant-transactional." +
        "fr-ec-cursor-pointer.fr-ec-button-max-width-reset." +
        "fr-ec-text-transform-all-caps")

    addtobag_obj[0].click()

    time.sleep(3)

    driver.get("https://www.uniqlo.com/us/en/cart")

    time.sleep(3)

    # Start collect information using scrapy

    sel = scrapy.Selector(text=driver.page_source)

    sel_data_order_summary = sel.css(
        "div.shared-global-ec-uikit-table-container.ordersummary-ec-cart")
    summary_order_total = sel_data_order_summary.css("h4::text")[3].get()
    summary_items_subtotal = sel_data_order_summary.css("span::text")[1].get()
    summary_shipping = sel_data_order_summary.css("span::text")[3].get()
    summary_subtotal = sel_data_order_summary.css("span::text")[5].get()
    summary_estimated_tax = sel_data_order_summary.css("span::text")[7].get()

    print("#################################################")
    print("summary_order_total ", summary_order_total)
    print("summary_items_subtotal ", summary_items_subtotal)
    print("summary_subtotal ", summary_subtotal)
    print("summary_estimated_tax ", summary_estimated_tax)
    print("summary_shipping ", summary_shipping)

    # Collect output in dict then convert to json and save it to csv file
    output_data = {}
    output_data["email"] = config.email
    output_data["subtotal"] = summary_items_subtotal
    output_data["estimated_shipping"] = summary_shipping
    output_data["estimated_tax"] = summary_estimated_tax
    output_data["total"] = summary_order_total

    with open(config.output_file, "a") as outfile:
        json.dump(output_data, outfile)
        outfile.write("\n")

    time.sleep(60)
    driver.quit()
