import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import json

from selenium.webdriver import ActionChains

class Order:
    def __init__(self, restaurantTenantId, cartId, orderTotal, orderDiscountTotal, orderGrandTotal, orderChannel, orderPaymentMode, orderSpecialInstructions, orderAppliedCoupon, customerTenantId, orderDeliveryAddress, isOrderAcceptedByRestaurant, isOrderPreparedByRestaurant, isOrderPaymentConfirmed, isOrderDelivered, restaurantOrderMode, orderTotalCgstPercentage, orderTotalSgstPercentage, isOrderOutForDelivery, isOrderCancelledByRestaurant, isOrderCancelledByCustomer, isOrderStartedPreparingByRestaurant, cancellationReason):
        self.restaurantTenantId = restaurantTenantId
        self.cartId = cartId
        self.orderTotal = orderTotal
        self.orderDiscountTotal = orderDiscountTotal
        self.orderGrandTotal = orderGrandTotal
        self.orderChannel = orderChannel
        self.orderPaymentMode = orderPaymentMode
        self.orderSpecialInstructions = orderSpecialInstructions
        self.orderAppliedCoupon = orderAppliedCoupon
        self.customerTenantId = customerTenantId
        self.orderDeliveryAddress = orderDeliveryAddress
        self.isOrderAcceptedByRestaurant = isOrderAcceptedByRestaurant
        self.isOrderPreparedByRestaurant = isOrderPreparedByRestaurant
        self.isOrderPaymentConfirmed = isOrderPaymentConfirmed
        self.isOrderDelivered = isOrderDelivered
        self.restaurantOrderMode = restaurantOrderMode
        self.orderTotalCgstPercentage = orderTotalCgstPercentage
        self.orderTotalSgstPercentage = orderTotalSgstPercentage
        self.isOrderOutForDelivery = isOrderOutForDelivery
        self.isOrderCancelledByRestaurant = isOrderCancelledByRestaurant
        self.isOrderCancelledByCustomer = isOrderCancelledByCustomer
        self.isOrderStartedPreparingByRestaurant = isOrderStartedPreparingByRestaurant
        self.cancellationReason = cancellationReason

def startChrome():
    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=/Users/ronik.basak/Library/Application Support/Google/Chrome/")
    driver = webdriver.Chrome(executable_path="/Users/ronik.basak/Documents/Ronik_Personal_Documents/D365/web-automation/integrate-online-pos/chromedriver-79", chrome_options=options)
    return driver

driver = startChrome()
url = 'https://partner.swiggy.com/orders'
driver.get(url)



# username = driver.find_element_by_css_selector("sign-up-form > div:nth-child(1) > input")
# password = driver.find_element_by_name("password")
# username.send_keys("197472")
# password.send_keys("sp27@12345")
# driver.find_element_by_id("sign-up-btn").click()

driver.find_element_by_xpath("//ul[@class='nav nav-tabs']/li[last()]/a").click()

order_list = driver.find_elements_by_css_selector('.order-preview.ng-scope')
order_count = 1

for order in order_list:
    print("****** SWIGGY ORDER "+str(order_count)+" ******")
    order_details = ''
    ActionChains(driver).move_to_element(order).click().perform()
    order_id = driver.find_element_by_css_selector('#print-more-details > h3 > span:nth-child(1) > span')
    print("Total Item Quantity:" + str(len(driver.find_elements_by_css_selector('.order-details-item-row.media'))))
    menu_list = driver.find_elements_by_css_selector('.order-details-item-row.media')
    item_quantity_list = driver.find_elements_by_css_selector('.order-details__item-quantity.should-animate')
    menu_seq = 0
    for menu in menu_list:
        print("Item Name: " + str(menu.find_element_by_css_selector('.media-body > span').text))
        item_name = str(menu.find_element_by_css_selector('.media-body > span').text)
        print("Item Category: " + str(menu.find_element_by_css_selector('.media-body > .order-details__item-category.ng-scope').text))
        print("Item Price:" + str(repr(menu.find_element_by_css_selector('.media-body > .order-details__item-price.ng-binding').text)).replace('u\'\u20b9', '').replace('\'',''))
        item_qty = str(item_quantity_list[menu_seq].text)
        print("Item Quantity: " + item_qty)
        menu_seq=menu_seq+1
        print("\n")
        order_details = order_details + str('Item Name: ' + item_name +
                    '   ' +
                    'Item Quantity: ' + item_qty +
                    '   ' + ',' + '\n')
    order_count=order_count+1
    order_total_css_selector = '#order-total-more-v2--' + str((order_id.text).replace('#', ''))
    order_grand_total = driver.find_elements_by_css_selector(order_total_css_selector)[0]
    print("Order Total:" + order_grand_total.text)
    swiggy_order = Order('RgVLcOjwZkG_1', 0, 0, 0, int(order_grand_total.text), 'swiggy', 'swiggy', order_details, '', 'XXXXXXXXXX', 'SELF', 1, 0, 1, 0,
                         'swiggy', 0, 0, 0, 0, 0, 1, '')
    # print(json.dumps(swiggy_order.__dict__))
    resp = requests.post('http://ec2-13-127-146-229.ap-south-1.compute.amazonaws.com:8082/api/restaurant-order/add',
                         data=json.dumps(swiggy_order.__dict__),
                         headers={'Content-Type':'application/json'})
    if resp.status_code != 200:
        # This means something went wrong.
        print("Exception: ")

# driver.quit()





# student = Student(first_name="Jake", last_name="Doyle")
# json_data = json.dumps(student.__dict__)
# print(json_data)
# print(Student(**json.loads(json_data)))
