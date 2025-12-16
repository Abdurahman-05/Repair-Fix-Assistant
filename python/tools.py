import os
from urllib import response
import requests
from tavily import TavilyClient


def get_exchange_rate(currency_code: str):
    """
    Retrieves the current exchange rate from ETB (Ethiopian Birr) to the target currency.
    Args:
        currency_code: The 3-letter currency code (e.g., 'USD', 'EUR').
    returns:
      Exchnage rate
    """
  

    rates = {
        "USD": 0.0065, 
        "EUR": 0.0078,
        "GBP": 0.0067
    }
    return rates.get(currency_code.upper(), "Unknown Currency")

def database_save(item: str, price: float):
    """
    Saves an item to the company database.
    Use this when the user explicitly asks to 'save', 'store', or 'buy' something.
    """
    print(f"\n💾 TOOL RUNNING: Saving '{item}' at price {price} to DB...")
    return "Success: Item saved."


def search_openfoodfacts(search_terms: str):
    """
    Searches ingredient list of a given product from OpenFoodFacts.
    
    Args:
        search_terms (str): Product name to search.
        
    Returns:
        str: Ingredient list or error message.
    """
    try:
        print("Looking in OpenFoodFacts API for:", search_terms)
        response = requests.get(
            f"https://world.openfoodfacts.org/api/v2/search?search_terms={search_terms}"
        )
        data = response.json()

        # Combine all ingredients_text into one string
        all_ingredients = ", ".join(
            product["ingredients_text"]
            for product in data.get("products", [])
            if "ingredients_text" in product
        )

        return all_ingredients

    except Exception as e:
        print("Error:", e)
        


def search_web(search_term : str):

  """
  Searchs the web to get realtime information
  Args:
    search_term: str
  returns:
     search result : str
  """

  tavily_client = TavilyClient(api_key="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")
  response = tavily_client.search(search_term)

  print(response)
  return str(response)
  # print(f"searching the web for", search_term)
print(search_web("who is the president of ethiopia?"))


# my_tools = [search_openfoodfacts, search_web]

  # api_key = os.getenv("TAVILY_API_KEY")

  # if not api_key:
  #   return "Error: TAVILY_API_KEY not found in .env file."
  # client = TavilyClient(api_key);
  # try:
  #   print("Web search response:", response)
  #   response = client.search(
  #     query= search_term
  #   )
  # except Exception as e:
  #   return f"Error during web search: {e}"
   
  # return str(response)