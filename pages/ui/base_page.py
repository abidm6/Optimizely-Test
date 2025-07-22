"""
Provides generic methods for interacting with application UI using selenium library at the core.
"""
import os
import time
import sys
import pytest
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.support.ui import Select, WebDriverWait


def wait_for(max_wait=15):
    time.sleep(max_wait)


class ElementAttributeToBe:
    """
    Checks whether element's attribute to be expected value.
    """
    def __init__(self, locator, attribute, expected_attribute_value):
        self.locator = locator
        self.attribute = attribute
        self.attribute_value = expected_attribute_value

    def __call__(self, driver, *args, **kwargs):
        expected_element = driver.find_element(*self.locator)
        attribute_value = expected_element.get_attribute(self.attribute)
        return self.attribute_value == attribute_value


class ElementCountToBeEqual:
    def __init__(self, locator, expected_count):
        self.locator = locator
        self.expected_count = expected_count

    def __call__(self, driver, *args, **kwargs):
        elements = driver.find_elements(*self.locator)
        element_count = len(elements)
        return element_count == self.expected_count


class ElementCountToBeEqualOrGrater:
    """
    Checks whether elements count is equal or greater.
    """
    def __init__(self, locator, expected_count):
        self.locator = locator
        self.expected_count = expected_count

    def __call__(self, driver, *args, **kwargs):
        elements = driver.find_elements(*self.locator)
        element_count = len(elements)
        return element_count >= self.expected_count


# pylint: disable=too-many-public-methods
class BasePage:
    """
    Contains methods for basic page interaction. All the methods are wrapper arround selenium
    webdriver methods.
    """

    def __init__(self, driver):
        self.driver = driver
        # Determine the correct modifier key based on the platform
        if sys.platform == "darwin": # 'darwin' is the platform name for macOS
            self.modifier_key = Keys.COMMAND
        else:
            self.modifier_key = Keys.CONTROL

    def get_current_url(self):
        return self.driver.current_url

    def get_element(self, by_locator, max_wait=120):
        self.wait_for_existence_of(by_locator, max_wait)
        return self.driver.find_element(*by_locator)

    def get_elements(self, by_locator, max_wait=120):
        return self.driver.find_elements(*by_locator)

    def get_element_above_of(self, reference_locator, target_locator):
        """
        :param reference_locator: this is the reference locator against which we need to find element above
        :param target_locator: the locator by which we need to find element above the reference locator
        :return: returns an element above the reference locator
        """
        reference_element = self.get_element(reference_locator)
        return self.driver.find_element(locate_with(*target_locator).above(reference_element))

    def get_element_below_of(self, reference_locator, target_locator):
        """
        :param reference_locator: this is the reference locator against which we need to find element below
        :param target_locator: the locator by which we need to find element below the reference locator
        :return: returns an element below the reference locator
        """
        reference_element = self.get_element(reference_locator)
        return self.driver.find_element(locate_with(*target_locator).below(reference_element))

    def get_element_to_left_of(self, reference_locator, target_locator):
        """
        :param reference_locator: this is the reference locator against which we need to find element to the left
        :param target_locator: the locator by which we need to find element to the left of the reference locator
        :return: returns an element which is to the left of the reference locator
        """
        reference_element = self.get_element(reference_locator)
        return self.driver.find_element(locate_with(*target_locator).to_left_of(reference_element))

    def get_element_to_right_of(self, reference_locator, target_locator):
        """
        :param reference_locator: this is the reference locator against which we need to find element to the right
        :param target_locator: the locator by which we need to find element to the right of the reference locator
        :return: returns an element which is to the right of the reference locator
        """
        reference_element = self.get_element(reference_locator)
        return self.driver.find_element(locate_with(*target_locator).to_right_of(reference_element))

    def get_parent_of(self, child_locator):
        element = self.get_element(child_locator)
        # return element.find_element((By.XPATH, '..'))
        return element.find_element(By.XPATH, './/parent::*')

    def get_attribute(self, locator, attribute):
        return self.get_element(locator).get_attribute(attribute).strip()

    def get_attribute_from_element(self, element, attribute):
        return element.get_attribute(attribute).strip()

    def get_property(self, locator, _property):
        return self.get_element(locator).get_property(_property).strip()

    def get_properties(self, locator):
        """
        Returns a dict of property & value pairs for the specified locator.

        Args:
            locator: locator of the desired element.
        """
        script = 'var items = {};' \
                 'var o = getComputedStyle(arguments[0]);' \
                 'for(var i = 0; i < o.length; i++){' \
                 'items[o[i]] = o.getPropertyValue(o[i]);}' \
                 'return items;'

        element = self.get_element(locator)

        return self.driver.execute_script(script, element)

    def get_list_of_text_from_locator(self, by_locator):
        elements = self.get_elements(by_locator)

        list_of_texts = [element.text.strip() for element in elements]

        return list_of_texts

    def get_list_of_text_from_elements(self, elements):
        """
        :param elements: list of elements from which text will be extracted
        :return: returns a list of texts/strings extracted from elements provided
        """
        list_of_texts = [element.text.strip() for element in elements]
        return list_of_texts

    def get_list_of_attributes_from_locator(self, by_locator, attribute):
        """
        Returns a specific attribute values for all elements found by given locator.

        Args:
            by_locator (_type_): the locator for which elements to be found.
            attribute (_type_): the attribute needs to find the value for.

        Returns:
            list: a list of values of the specified attribute.
        """
        elements = self.get_elements(by_locator)
        list_of_values = [element.get_attribute(attribute).strip() for element in elements]
        return list_of_values

    def get_total_count(self, by_locator, max_wait=60):
        """
        :param by_locator: the locator for which total items to be counted/found
        :param max_wait: time to find the required element by locator
        :return: return the total number of elements found for that specific locator
        """
        return len(self.get_elements(by_locator, max_wait))

    def get_text_by_locator(self, locator, max_wait=15):
        """
        :param locator: the locator for which text is to be extracted
        :param max_wait: max wait time to find the required element by locator
        :return: returns a trimmed/stripped string for element located by provided locator
        """
        return self.get_element(locator, max_wait).text.strip()

    def get_text_by_element(self, element):
        """
        Returns string from element provided.
        :param element: element for which text is to be extracted
        :return: returns stripped text/string from element provided
        """
        return element.text.strip()

    def get_list_of_texts_for_element(self, locator):
        """
        Get texts for all elements found by specified locator.
        :param locator: the locator for which text list to be extracted.
        :return: list of text.
        """
        return [item.text.strip() for item in self.get_elements(locator)]

    def get_css_value(self, locator, css_property):
        """
        Get css value for a css property i.e.: color, background-color, padding etc.
        :param locator: locator by which element's css property to be extracted
        :param css_property: the css property for which value to be extracted
        :return: returns css property value after stripping it off.
        """
        expected_element = self.get_element(locator)
        return expected_element.value_of_css_property(css_property).strip()

    def get_css_value_from_element(self, expected_element, css_property):
        """
        Get css value for a css property i.e.: color, background-color, padding etc.
        :param expected_element: element for which element's css property to be extracted
        :param css_property: the css property for which value to be extracted
        :return: returns css property value after stripping it off.
        """
        return expected_element.value_of_css_property(css_property).strip()

    def click_and_wait(self, by_locator, wait_time=0, max_wait_for_clickable=120):
        """
        Clicks an element for provided locator & wait for a specified amount of time.
        :param by_locator: locator for which element to be clicked
        :param wait_time: wait after click on the element. wait time is in second
        :param max_wait_for_clickable: maximum waiting time for element to clickable
        :return: returns nothing
        """
        self.wait_for_element_to_clickable(by_locator, max_wait=max_wait_for_clickable)
        self.driver.find_element(*by_locator).click()
        time.sleep(wait_time)

    def click_and_wait_by_element(self, element, wait_time=0, max_wait_for_clickable=120):
        """
        Click on provided element & wait for a specified amount of time.
        :param element: element for which element to be clicked
        :param wait_time: wait after click on the element. wait time is in second
        :param max_wait_for_clickable: maximum waiting time for element to clickable
        :return: returns nothing
        """
        self.wait_for_element_to_clickable(element, max_wait=max_wait_for_clickable)
        element.click()
        time.sleep(wait_time)

    def get_selected_text_from_dropdown(self, dropdown_locator):
        """
        Gets the first selected options from the desired dropdown.

        Args:
            dropdown_locator (_type_): Locator for the dropdown.

        Returns:
            str: Returns the first selected option as string.
        """
        select = Select(self.get_element(dropdown_locator))
        return select.first_selected_option.text.strip()

    def get_all_options_from_dropdown(self, dropdown_locator):
        """
        Gets all the options (visible text) from the desired dropdown.

        Args:
            dropdown_locator (_type_): Locator for the dropdown.

        Returns:
            str: Returns all options from dropdown.
        """
        select = Select(self.get_element(dropdown_locator))
        return self.get_list_of_text_from_elements(select.options)

    def click_and_wait_for_target(self, by_locator, target_locator=None):
        """
        Clicks an element for provided locator & wait for a specific element located by target locator.
        :param by_locator: locator for which element to be clicked
        :param target_locator: the locator for which to wait for before throwing ELEMENT NOT FOUND EXCEPTION
        :return: returns nothing
        """
        self.click_and_wait(by_locator)
        if target_locator is not None:
            self.wait_for_existence_of(target_locator)

    def hover(self, by_locator, wait_time=0):
        element = self.get_element(by_locator)
        ActionChains(self.driver).move_to_element(element).perform()
        time.sleep(wait_time)

    def hover_element(self, by_element, wait_time=0):
        ActionChains(self.driver).move_to_element(by_element).perform()
        time.sleep(wait_time)

    def hover_and_click(self, by_locator):
        element = self.get_element(by_locator)
        ActionChains(self.driver).move_to_element(element).click().perform()

    def hover_and_click_by_element(self, element):
        ActionChains(self.driver).move_to_element(element).click().perform()

    def hover_and_double_click_by_element(self, element):
        ActionChains(self.driver).move_to_element(element).double_click().perform()

    def clear_field(self, by_locator):
        self.enter_text_at('', by_locator)

    def press_back_space(self, by_locator):
        self.get_element(by_locator).send_keys(Keys.BACK_SPACE)

    def press_arrow_up(self, by_locator):
        self.get_element(by_locator).send_keys(Keys.ARROW_UP)

    def press_arrow_left(self, by_locator):
        self.get_element(by_locator).send_keys(Keys.ARROW_LEFT)

    def press_arrow_right(self, by_locator):
        self.get_element(by_locator).send_keys(Keys.ARROW_RIGHT)

    def press_arrow_down(self, by_locator):
        self.get_element(by_locator).send_keys(Keys.ARROW_DOWN)

    def clear_field_and_send_keys(self, data, target_locator):
        element = self.get_element(target_locator)
        element.clear()
        element.send_keys(data)

    def press_enter(self, target_locator=None):
        if target_locator is None:
            actions = ActionChains(self.driver)
            actions.key_down(Keys.ENTER).key_up(Keys.ENTER).perform()
        else:
            element = self.get_element(target_locator)
            element.send_keys(Keys.ENTER)

    def press_escape(self):
        action = ActionChains(self.driver)
        action.send_keys(Keys.ESCAPE).perform()

    def press_ctrl_and_a(self, target_locator, max_wait=5):
        element = self.get_element(target_locator, max_wait)
        element.send_keys(self.modifier_key + 'a')

    def delete_field(self, target_locator):
        element = self.get_element(target_locator)
        element.send_keys(self.modifier_key + 'a')
        element.send_keys(Keys.DELETE)

    def element_is_displayed(self, target_locator):
        element = self.get_element(target_locator)
        res = element.is_displayed()
        return res

    def scroll_to_element(self, target_locator):
        element = self.get_element(target_locator)
        actions = ActionChains(self.driver)
        actions.move_to_element(element)
        actions.perform()

    def click_and_wait_for_invisibility(self, by_locator, max_wait=120):
        self.click_and_wait(by_locator)
        self.wait_for_invisibility_of(by_locator, max_wait)

    def enter_text_in_notes(self, text):
        self.wait_for_visibility_of(self.notes, 30)
        self.enter_text_at(text, self.notes)

    def enter_text_at(self, text, target_locator, clear_existing=True):
        """
        Enter text into specific element located by a target locator. If clear_existing=True then existing text
        will be cleared out & new text is entered. Otherwise, new text is entered at the end of existing text.

        :param text: text to be entered
        :param target_locator: locator for which text to be entered
        :param clear_existing: if set to True existing content/data is cleared before entering new data.
        :return: returns nothing
        """
        self.wait_for_visibility_of(target_locator)
        element = self.get_element(target_locator)

        if clear_existing:
            element.clear()
        else:
            actions = ActionChains(self.driver)
            actions.key_down(Keys.LEFT_CONTROL).key_down(Keys.END) \
                .key_up(Keys.LEFT_CONTROL).key_up(Keys.END).perform()
        element.send_keys(text)

    def select_by_visible_text(self, locator, text_to_select):
        """
        Select item from a dropdown menu by visible text.
        :param locator: dropdown locator to which specific item to be selected
        :param text_to_select: text to be selected
        :return: returns nothing
        """
        if not text_to_select or text_to_select != '':
            select = Select(self.get_element(locator))
            select.select_by_visible_text(text_to_select)
        else:
            print(f'No selectable item {text_to_select} found...')

    def select_by_partial_visible_text(self, locator: tuple, partial_text: str):
        """
        Select an item from a dropdown where the visible text contains a given substring.
        
        :param locator: dropdown locator (tuple format: (By.METHOD, "locator string"))
        :param partial_text: part of the visible text to match
        """
        if not partial_text:
            print(f"No selectable item text provided: '{partial_text}'")
            return

        select = Select(self.get_element(locator))
        matched = False

        for option in select.options:
            option_text = option.text.strip()
            if partial_text in option_text:
                select.select_by_visible_text(option_text)
                matched = True
                break

        if not matched:
            raise ValueError(f"No matching dropdown option containing '{partial_text}' found.")


    def select_by_value(self, locator, value_to_select):
        """
        Select item from a dropdown menu by value.
        :param locator: dropdown locator to which specific item to be selected
        :param value_to_select: value to be selected
        :return: returns nothing
        """
        if not value_to_select or value_to_select != '':
            select = Select(self.get_element(locator))
            select.select_by_value(value_to_select)
        else:
            print(f'No selectable item {value_to_select} found...')

    def wait_for_expected_condition(self, condition, max_wait=120):
        """
        Wait for specified time until provided CONDITION is met.
        :param condition: condition for which we must wait until specified amount of time
        :param max_wait: maximum time to wait for the CONDITION to be satisfied
        :return: nothing
        """
        wait = WebDriverWait(self.driver, max_wait)
        wait.until(condition)

    def wait_for_existence_of(self, locator, max_wait=120):
        """
        Wait for an element for its existence upto specified time.

        Args:
            locator (_type_): the locator for the expected element.
            max_wait (int, optional): maximum wait time before throwing an exception. Defaults to 120.
        """
        self.wait_for_expected_condition(EC.presence_of_element_located(locator), max_wait)

    def wait_for_visibility_of(self, locator, max_wait=120):
        """
        Wait for the visibility of an element located by specified locator until maximum time expire

        :param locator: the locator for which we need to wait
        :param max_wait: the time we need to wait for until the element is visible for the locator
        :return:
        """
        self.wait_for_expected_condition(EC.visibility_of_element_located(locator), max_wait)

    def wait_for_visibility_of_element(self, element, max_wait=120):
        """
        Wait for the visibility of an element located by specified locator until maximum time expire

        :param element: the locator for which we need to wait
        :param max_wait: the time we need to wait for until the element is visible for the locator
        :return:
        """
        self.wait_for_expected_condition(EC.visibility_of(element), max_wait)

    def wait_for_invisibility_of(self, locator, max_wait=120):
        """
        Wait for the invisibility of an element located by specified locator until maximum time expire
        :param locator: the locator for which we need to wait
        :param max_wait: the time we need to wait for until the element is invisible for the locator
        :return: returns nothing
        """
        self.wait_for_expected_condition(EC.invisibility_of_element_located(locator), max_wait)

        return True

    def wait_for_visibility_of_text(self, locator, text, max_wait=120):
        """
        Wait for a specific text to be present in the DOM upto maxium wait time.

        Args:
            locator: the locator for the expeced element.
            text: the text to be waiting for its visibility in the DOM.
            max_wait (int, optional): maximum time to wait for the visibility of the expected text. Defaults to 120.

        Returns:
            boolean: Returns True upon success.
        """
        self.wait_for_expected_condition(EC.text_to_be_present_in_element(locator, text), max_wait)

        return True

    def text_to_be_not_present_in_element(self, locator, text_):
        """ An expectation for checking if the given text is present in the
        specified element.
        locator, text
        """

        def _predicate(driver):
            try:
                element_text = driver.find_element(*locator).text
                return text_ not in element_text
            except StaleElementReferenceException:
                return False

        return _predicate

    def text_to_be_not_present_in_web_element(self, element, text, second):
        """ An expectation for checking if the given text is present in the
        specified element.
        locator, text
        """
        for _ in range(second):
            try:
                if text not in self.get_text_by_element(element):
                    return True
            except Exception as e:
                print('An exception occurred:', e)
            time.sleep(1)
        return False

    def wait_for_invisibility_of_text(self, locator, text, max_wait=120):
        self.wait_for_expected_condition(self.text_to_be_not_present_in_element(locator, text), max_wait)
        return True

    def text_to_be_present_in_web_element(self, element, text, second):
        """ An expectation for checking if the given text is present in the
        specified element.
        locator, text
        """
        for _ in range(second):
            try:
                if text in self.get_text_by_element(element):
                    return True
            except Exception as e:
                print('An exception occurred:', e)
            time.sleep(1)
        return False

    def wait_for_element_to_clickable(self, locator, max_wait=120):
        self.wait_for_expected_condition(EC.element_to_be_clickable(locator), max_wait)

    def wait_for_element_count_to_be(self, locator, expected_count, max_wait=120):
        expected_condition = ElementCountToBeEqual(locator, expected_count)
        self.wait_for_expected_condition(expected_condition, max_wait)

    def wait_for_attribute_to_be(self, locator, attribute, attribute_value):
        condition = ElementAttributeToBe(locator, attribute, attribute_value)
        self.wait_for_expected_condition(condition)

    def wait_until_attribute_contains(self, element, attribute, attribute_value, timeout=10):
        try:
            if isinstance(element, WebElement):
                self.wait_for_expected_condition(
                    lambda driver: attribute_value in self.get_attribute_from_element(element, attribute),
                    max_wait=timeout
                )
            else:
                self.wait_for_expected_condition(
                    lambda driver: attribute_value in self.get_attribute(element, attribute),
                    max_wait=timeout
                )
        except TimeoutException:
            print(f"Timed out waiting for class value '{attribute_value}'")

    def wait_until_attribute_not_contains(self, element, attribute, attribute_value, timeout=10):
        try:
            if isinstance(element, WebElement):
                self.wait_for_expected_condition(
                    lambda driver: attribute_value not in self.get_attribute_from_element(element, attribute),
                    max_wait=timeout
                )
            else:
                self.wait_for_expected_condition(
                    lambda driver: attribute_value not in self.get_attribute(element, attribute),
                    max_wait=timeout
                )
        except TimeoutException:
            print(f"Timed out waiting for remove class value '{attribute_value}'")


    def is_element_visible(self, locator, wait_time=60):
        """
        Checks for an element for its visibility & return True if it's visible.
        :param locator: locator for the element to wait for visibility.
        :param wait_time: maximum wait time for the element's visibility.
        :return: True/False
        """

        if isinstance(locator, WebElement):
            try:
                self.wait_for_expected_condition(EC.visibility_of(locator), wait_time)
                return True
            except TimeoutException:
                return False
        try:
            self.wait_for_visibility_of(locator, wait_time)
            return True
        except TimeoutException:
            return False
        
    def is_element_clickable(self, locator, max_wait=5):
        try:
            # Wait until the dropdown is clickable (element is visible, enabled, and not obscured)
            WebDriverWait(self.driver, max_wait).until(
                EC.element_to_be_clickable(locator)
            )
            return True
        except:
            return False

    def is_element_clickable(self, locator, wait_time=60):
        """
        Checks for an element if it is clickable & return True if it's clickable.
        :param locator: locator for the element to wait for clickable.
        :param wait_time: maximum wait time for the element's clickable.
        :return: True/False
        """
        try:
            self.wait_for_element_to_clickable(locator, wait_time)
            return True
        except TimeoutException:
            return False

    def select_item_from_selection_list(self, locator, expected_item):
        selection_items = self.get_elements(locator)
        for item in selection_items:
            if self.get_text_by_element(item) == expected_item:
                item.click()
                print(f'Selection item {expected_item.upper()} selected.')
                break

    def get_pseudo_element_property_value(self, locator, expected_pseudo_element, expected_pseudo_property):
        js_script = f'return window.getComputedStyle(document.querySelector("{locator}"),' \
                    f'":{expected_pseudo_element}").getPropertyValue("{expected_pseudo_property}")'
        return self.driver.execute_script(js_script)

    def get_js_executed_result(self, element_identifier, _type):
        js_script = f'return document.querySelector("{element_identifier}").{_type};'
        return self.driver.execute_script(js_script)

    def scroll_into_view(self, locator):
        element = self.get_element(locator)
        self.driver.execute_script('arguments[0].scrollIntoView();', element)

    def scroll_into_view_by_element(self, element):
        self.driver.execute_script('arguments[0].scrollIntoView();', element)

    def drag_item_by_offset(self, source_locator, x_offset, y_offset):
        actions = ActionChains(self.driver)
        actions.drag_and_drop_by_offset(self.get_element(source_locator), x_offset, y_offset).perform()
        time.sleep(1)

    def click_element_by_offset(self, locator, x_offset, y_offset):
        element = self.get_element(locator)
        actions = ActionChains(self.driver)
        actions.move_to_element_with_offset(element, x_offset, y_offset).click().perform()

    def drag_mouse_from_one_element_to_another(self, source_locator, destination_locator):
        source_element = self.get_element(source_locator)
        destination_element = self.get_element(destination_locator)

        actions = ActionChains(self.driver)
        actions.drag_and_drop(source_element, destination_element).perform()

    def use_keyboard_shortcut(self, key):
        actions = ActionChains(self.driver)
        actions.key_down(Keys.LEFT_CONTROL).key_down(Keys.LEFT_ALT) \
            .send_keys(key).key_up(Keys.LEFT_CONTROL).key_up(Keys.LEFT_ALT).perform()

    def perform_double_click_on(self, locator):
        actions = ActionChains(self.driver)
        actions.double_click(self.get_element(locator)).perform()

    def perform_right_click_on(self, element):
        """
        Performs a right click/context click on a desired element by its locator.

        :param element: locator of the desired element.
        :return: None
        """
        actions = ActionChains(self.driver)
        actions.context_click(element).perform()

    # right Click
    def right_click(self, locator):
        element = self.get_element(locator)
        right_click = ActionChains(self.driver).move_to_element(element)
        right_click.context_click().perform()

    def get_current_window_handle(self):
        return self.driver.current_window_handle

    def switch_to_window(self, window_identifier=1):
        """
        Switches to window by its position or window handle. First window position is 1, second window is 2 etc.

        :param window_identifier: position of the window or window handle
        """
        if isinstance(window_identifier, int):
            self.driver.switch_to.window(self.driver.window_handles[window_identifier - 1])
        elif isinstance(window_identifier, str):
            self.driver.switch_to.window(window_identifier)
        else:
            print('Invalid window type provided...')

    def change_frame(self, frame_identifier, max_wait=60):
        if isinstance(frame_identifier, int):
            self.driver.switch_to.frame(self.get_elements((By.TAG_NAME, 'iframe'))[frame_identifier])
            print(f'Frame switched by using id/index {frame_identifier}...')
        elif isinstance(frame_identifier, str):
            self.wait_for_expected_condition(EC.frame_to_be_available_and_switch_to_it((By.ID,
                                                                                        frame_identifier)), max_wait)
            print(f'Frame switched by using ID {frame_identifier}...')
        else:
            self.wait_for_expected_condition(
                EC.frame_to_be_available_and_switch_to_it(self.get_element(frame_identifier)), max_wait)
            print(f'Frame switched by using locator {frame_identifier}...')
        time.sleep(2)

    def wait_for_alert_window_present(self, max_wait=30):
        self.wait_for_expected_condition(EC.alert_is_present(), max_wait=max_wait)

    def accept_alert(self):
        alert = self.driver.switch_to.alert
        alert.accept()

    def dismiss_alert(self):
        alert = self.driver.switch_to.alert
        alert.dismiss()

    def back_to_default_content(self):
        self.driver.switch_to.default_content()

    def get_css_property(self, attribute, locator):
        element = self.get_element(locator)
        val = element.value_of_css_property(attribute)
        # print(val)
        return val

    def get_background_color(self, locator):
        return self.get_css_value(locator, 'background-color')

    def get_border_color(self, locator):
        return self.get_css_value(locator, 'border-color')

    def paste_text_in_input_field_by_locator(self, locator):
        self.click_and_wait(locator, 1)
        # self.Press_Ctrl_And_V(locator)
        ActionChains(self.driver).key_down(self.modifier_key).send_keys('v').key_up(self.modifier_key).perform()

    def get_element_by_text(self, text):
        locator = (By.XPATH, f'//*[contains(text(),"{text}")]')
        return self.get_element(locator, 3)

    def get_elements_by_text(self, text):
        locator = (By.XPATH, f'//*[contains(text(),"{text}")]')
        return self.get_elements(locator)

    @staticmethod
    def toggle_network(enable=True):
        password = pytest.configs.get_config('local_password')
        import platform
        os_name = platform.system()
        if os_name == 'Darwin':
            if enable:
                os.system(f'echo {password} | sudo -S networksetup -setnetworkserviceenabled Wi-Fi on')
            else:
                os.system(f'echo {password} | sudo -S networksetup -setnetworkserviceenabled Wi-Fi off')
        elif os_name == 'Linux':
            if enable:
                os.system('enable_network')
            else:
                os.system('disable_network')

    def disable_network(self):
        self.toggle_network(enable=False)
        print('Network disconnected...\n')

    def enable_network(self):
        self.toggle_network(enable=True)
        print('Network connected...\n')

    def slow_type(self, locator, text, delay=0.1):
        """Send a text to an element one character at a time with a delay."""
        self.wait_for_visibility_of(locator)
        element = self.get_element(locator)
        for character in text:
            element.send_keys(character)
            time.sleep(delay)

    def copy_text_from_locator(self, locator):
        # create action chain object
        action = ActionChains(self.driver)
        self.press_ctrl_and_a(locator)
        action.key_down(self.modifier_key).send_keys('C').key_up(self.modifier_key).perform()
