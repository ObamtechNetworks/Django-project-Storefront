from locust import HttpUser, task, between
from random import randint

class WebsiteUser(HttpUser):
    # Viewing products
    wait_time = between(1, 5) # Simulate user wait time between tasks, 1 to 5 seconds
    
    @task(2) # Adding weights to the task
    def view_products(self):
        print("Viewing products")
        collection_id = randint(2, 6)
        self.client.get(
            f"/store/products/?collection_id={collection_id}",
            name="/store/products")
    
    # Viewing product details
    @task(4)
    def view_product(self):
        print("Viewing product details")
        product_id = randint(1, 1000)
        self.client.get(
            f"/store/products/{product_id}/",
            name="/store/products/:id")
    
    # Adding products to cart
    @task(1)
    def add_to_cart(self):
        print("Adding product to cart")
        product_id = randint(1, 10)
        self.client.post(
            f'/store/carts/{self.cart_id}/items/',
            name='/store/carts/items',
            json={'product_id': product_id, 'quantity': 1},
        )

    # a lifecycle hook that runs when a simulated user starts a session
    def on_start(self):
        # Create a new cart when a user starts a session
        response = self.client.post("/store/carts/")
        result = response.json()
        self.cart_id = result["id"]
    
    # @task
    # def say_hello(self):
    #     print("Hello, welcome to the store!")
    #     self.client.get("/playground/hello/")