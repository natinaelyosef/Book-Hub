{% extends 'customer/base.html' %}

{% block content %}
<div class="container" style="max-width: 800px; margin: 0 auto;">
    <h1 style="color: #2c3e50; margin-bottom: 30px;">
        <i class="fas fa-shopping-cart"></i> Checkout
    </h1>
    
    {% if messages %}
    <div style="margin-bottom: 20px;">
        {% for message in messages %}
        <div class="alert alert-{{ message.tags }}">
            {{ message }}
        </div>
        {% endfor %}
    </div>
    {% endif %}
    
    <div class="checkout-container" style="background: white; border-radius: 12px; padding: 30px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
        <!-- Order Summary -->
        <div class="order-summary" style="margin-bottom: 30px;">
            <h3 style="color: #2c3e50; margin-bottom: 20px; border-bottom: 2px solid #ecf0f1; padding-bottom: 10px;">
                <i class="fas fa-receipt"></i> Order Summary
            </h3>
            
            <div id="cart-items">
                {% for item in rental_items %}
                <div class="cart-item" style="display: flex; justify-content: space-between; align-items: center; padding: 15px 0; border-bottom: 1px solid #f1f2f6;">
                    <div>
                        <h4 style="margin: 0; color: #2c3e50;">{{ item.title }}</h4>
                        <p style="margin: 5px 0; color: #7f8c8d;">by {{ item.author }} • Rental</p>
                    </div>
                    <div style="text-align: right;">
                        <p style="margin: 0; font-weight: 600; color: #2c3e50;">${{ item.rental_price }}/day</p>
                    </div>
                </div>
                {% endfor %}
                
                {% for item in purchase_items %}
                <div class="cart-item" style="display: flex; justify-content: space-between; align-items: center; padding: 15px 0; border-bottom: 1px solid #f1f2f6;">
                    <div>
                        <h4 style="margin: 0; color: #2c3e50;">{{ item.title }}</h4>
                        <p style="margin: 5px 0; color: #7f8c8d;">by {{ item.author }} • Purchase</p>
                    </div>
                    <div style="text-align: right;">
                        <p style="margin: 0; font-weight: 600; color: #2c3e50;">${{ item.sale_price }}</p>
                    </div>
                </div>
                {% endfor %}
            </div>
            
            <div class="totals" style="margin-top: 20px; padding-top: 20px; border-top: 2px solid #ecf0f1;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <span>Subtotal:</span>
                    <span style="font-weight: 600;">${{ total }}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <span>Delivery Fee:</span>
                    <span style="font-weight: 600;" id="delivery-fee">$0.00</span>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 1.2rem; font-weight: 700; color: #2c3e50; padding-top: 10px; border-top: 1px solid #ecf0f1;">
                    <span>Total:</span>
                    <span id="total-amount">${{ total }}</span>
                </div>
            </div>
        </div>
        
        <!-- Order Form -->
        <form id="order-form" method="POST" action="{% url 'create_order' %}">
            {% csrf_token %}
            
            <!-- Order Type -->
            <div class="form-section" style="margin-bottom: 25px;">
                <h3 style="color: #2c3e50; margin-bottom: 15px;">
                    <i class="fas fa-tag"></i> Order Type
                </h3>
                <div style="display: flex; gap: 20px; align-items: center;">
                    {% if rental_items %}
                    <div>
                        <input type="radio" id="rent" name="order_type" value="rent" checked>
                        <label for="rent" style="margin-left: 5px;">Rental</label>
                    </div>
                    {% endif %}
                    {% if purchase_items %}
                    <div>
                        <input type="radio" id="buy" name="order_type" value="buy" {% if not rental_items %}checked{% endif %}>
                        <label for="buy" style="margin-left: 5px;">Purchase</label>
                    </div>
                    {% endif %}
                </div>
                
                <!-- Rental Duration (shown only for rentals) -->
                <div id="rental-duration" style="margin-top: 15px; {% if not rental_items %}display: none;{% endif %}">
                    <label for="rental_days" style="display: block; margin-bottom: 5px; font-weight: 500;">Rental Duration:</label>
                    <select id="rental_days" name="rental_days" style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 8px;">
                        <option value="7">7 days</option>
                        <option value="14">14 days</option>
                        <option value="30">30 days</option>
                    </select>
                </div>
            </div>
            
            <!-- Delivery Options -->
            <div class="form-section" style="margin-bottom: 25px;">
                <h3 style="color: #2c3e50; margin-bottom: 15px;">
                    <i class="fas fa-truck"></i> Delivery Options
                </h3>
                
                <div style="margin-bottom: 15px;">
                    <input type="radio" id="pickup" name="delivery_option" value="pickup" checked>
                    <label for="pickup" style="margin-left: 5px; font-weight: 500;">
                        <i class="fas fa-store"></i> Store Pickup (Free)
                    </label>
                    <p style="margin: 5px 0 0 25px; color: #7f8c8d; font-size: 0.9rem;">
                        Pick up your order from the store during business hours
                    </p>
                </div>
                
                <div>
                    <input type="radio" id="delivery" name="delivery_option" value="delivery">
                    <label for="delivery" style="margin-left: 5px; font-weight: 500;">
                        <i class="fas fa-home"></i> Home Delivery (+$3.00)
                    </label>
                    <p style="margin: 5px 0 0 25px; color: #7f8c8d; font-size: 0.9rem;">
                        Get your order delivered to your doorstep
                    </p>
                </div>
                
                <!-- Delivery Address (shown only for delivery) -->
                <div id="delivery-details" style="margin-top: 15px; display: none;">
                    <div style="margin-bottom: 15px;">
                        <label for="delivery_address" style="display: block; margin-bottom: 5px; font-weight: 500;">Delivery Address:</label>
                        <textarea id="delivery_address" name="delivery_address" rows="3" style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 8px;" placeholder="Enter your complete address"></textarea>
                    </div>
                    
                    <div>
                        <label for="preferred_time" style="display: block; margin-bottom: 5px; font-weight: 500;">Preferred Time:</label>
                        <select id="preferred_time" name="preferred_time" style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 8px;">
                            <option value="">Any Time</option>
                            <option value="morning">Morning (9AM - 12PM)</option>
                            <option value="afternoon">Afternoon (12PM - 4PM)</option>
                            <option value="evening">Evening (4PM - 8PM)</option>
                        </select>
                    </div>
                </div>
            </div>
            
            <!-- Payment Note -->
            <div class="payment-note" style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 25px;">
                <h4 style="color: #2c3e50; margin-bottom: 10px;">
                    <i class="fas fa-info-circle"></i> Payment Information
                </h4>
                <p style="color: #7f8c8d; margin: 0;">
                    💡 <strong>Pay when you receive the book</strong> (cash or card)<br>
                    The store will contact you to confirm payment method
                </p>
            </div>
            
            <!-- Additional Notes -->
            <div class="form-section" style="margin-bottom: 25px;">
                <label for="notes" style="display: block; margin-bottom: 5px; font-weight: 500;">
                    <i class="fas fa-sticky-note"></i> Additional Notes (Optional):
                </label>
                <textarea id="notes" name="notes" rows="3" style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 8px;" placeholder="Any special instructions for your order..."></textarea>
            </div>
            
            <!-- Hidden Fields -->
            <input type="hidden" id="total_amount" name="total_amount" value="{{ total }}">
            <input type="hidden" id="delivery_fee" name="delivery_fee" value="0">
            
            <!-- Action Buttons -->
            <div style="display: flex; gap: 15px; margin-top: 30px;">
                <a href="{% url 'shopping_cart' %}" class="btn" style="background-color: #95a5a6; color: white; padding: 12px 25px; text-decoration: none; border-radius: 8px; font-weight: 600; flex: 1; text-align: center;">
                    <i class="fas fa-arrow-left"></i> Back to Cart
                </a>
                <button type="submit" class="btn" style="background-color: #2ecc71; color: white; padding: 12px 25px; border: none; border-radius: 8px; font-weight: 600; flex: 2; cursor: pointer;">
                    <i class="fas fa-check-circle"></i> Place Order
                </button>
            </div>
        </form>
    </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    // Toggle rental duration
    const orderTypeRadios = document.querySelectorAll('input[name="order_type"]');
    const rentalDurationDiv = document.getElementById('rental-duration');
    
    orderTypeRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            if (this.value === 'rent') {
                rentalDurationDiv.style.display = 'block';
            } else {
                rentalDurationDiv.style.display = 'none';
            }
        });
    });
    
    // Toggle delivery details
    const deliveryOptionRadios = document.querySelectorAll('input[name="delivery_option"]');
    const deliveryDetailsDiv = document.getElementById('delivery-details');
    const deliveryFeeSpan = document.getElementById('delivery-fee');
    const totalAmountSpan = document.getElementById('total-amount');
    const totalAmountInput = document.getElementById('total_amount');
    const deliveryFeeInput = document.getElementById('delivery_fee');
    
    const subtotal = {{ total }};
    
    deliveryOptionRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            if (this.value === 'delivery') {
                deliveryDetailsDiv.style.display = 'block';
                deliveryFeeSpan.textContent = '$3.00';
                const newTotal = subtotal + 3.0;
                totalAmountSpan.textContent = '$' + newTotal.toFixed(2);
                totalAmountInput.value = newTotal.toFixed(2);
                deliveryFeeInput.value = '3.00';
            } else {
                deliveryDetailsDiv.style.display = 'none';
                deliveryFeeSpan.textContent = '$0.00';
                totalAmountSpan.textContent = '$' + subtotal.toFixed(2);
                totalAmountInput.value = subtotal.toFixed(2);
                deliveryFeeInput.value = '0.00';
            }
        });
    });
    
    // Update total when rental days change
    const rentalDaysSelect = document.getElementById('rental_days');
    rentalDaysSelect.addEventListener('change', function() {
        // Recalculate rental total based on days
        let rentalTotal = 0;
        document.querySelectorAll('#cart-items .cart-item').forEach(item => {
            const priceText = item.querySelector('p:last-child').textContent;
            if (priceText.includes('/day')) {
                const pricePerDay = parseFloat(priceText.replace('$', '').replace('/day', ''));
                rentalTotal += pricePerDay * parseInt(this.value);
            }
        });
        
        // Update totals
        const deliveryFee = parseFloat(deliveryFeeInput.value);
        const newTotal = rentalTotal + {{ purchase_total|default:0 }} + deliveryFee;
        totalAmountSpan.textContent = '$' + newTotal.toFixed(2);
        totalAmountInput.value = newTotal.toFixed(2);
    });
    
    // Form submission (normal POST to Django view)
    const orderForm = document.getElementById('order-form');
    orderForm.addEventListener('submit', function(e) {
        const deliveryOption = document.querySelector('input[name="delivery_option"]:checked').value;
        if (deliveryOption === 'delivery') {
            const deliveryAddress = document.getElementById('delivery_address').value.trim();
            if (!deliveryAddress) {
                e.preventDefault();
                alert('Please enter your delivery address');
            }
        }
    });
});
</script>

<style>
.alert {
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 15px;
}

.alert-success {
    background-color: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
}

.alert-error {
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
}

.alert-warning {
    background-color: #fff3cd;
    color: #856404;
    border: 1px solid #ffeaa7;
}

.btn:hover {
    opacity: 0.9;
    transform: translateY(-2px);
    transition: all 0.3s;
}
</style>
{% endblock %}
