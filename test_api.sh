#!/bin/bash
# test_api.sh
# Comprehensive REST Cart API Testing Script (CRUD: Create/Read/Update/Delete)

# --- Configuration ---
HOST="http://localhost:8000"
COOKIE_FILE="curl_cookies.txt"
PRODUCT_ID=1
INITIAL_QUANTITY=2
UPDATE_QUANTITY=5 # New quantity for the update test
JSON_DATA_ADD="{\"product_id\": ${PRODUCT_ID}, \"quantity\": ${INITIAL_QUANTITY}}"
JSON_DATA_UPDATE="{\"product_id\": ${PRODUCT_ID}, \"quantity\": ${UPDATE_QUANTITY}}"

# Ensure the cookie file is removed from previous runs
rm -f $COOKIE_FILE

echo "--- Starting Cart API Test Suite ---"
echo "Product ID being tested: $PRODUCT_ID"
echo "-----------------------------------------"

# ----------------- 1. ADD ITEM (POST /api/cart/) -----------------
echo "1. POST: Adding item (initial quantity: ${INITIAL_QUANTITY})..."
RESPONSE=$(curl -s -X POST -c $COOKIE_FILE -H "Content-Type: application/json" -d "$JSON_DATA_ADD" "$HOST/api/cart/")
echo "   Response: $RESPONSE"

if [[ $RESPONSE == *'"cart_length":2'* ]]; then
    echo "   Success: Item added."
else
    echo "   Error: Failed to add initial item. Exiting."
    exit 1
fi
echo "-----------------------------------------"

# ----------------- 2. UPDATE ITEM (POST /api/cart/) -----------------
echo "2. POST: Updating item quantity from ${INITIAL_QUANTITY} to ${UPDATE_QUANTITY}..."
# Using -b (read cookie) here to ensure we use the same session created in step 1
RESPONSE=$(curl -s -X POST -b $COOKIE_FILE -H "Content-Type: application/json" -d "$JSON_DATA_UPDATE" "$HOST/api/cart/")
echo "   Response: $RESPONSE"

# Check if the response confirms the update quantity (5)
if [[ $RESPONSE == *'"cart_length":5'* ]]; then
    echo "   Success: Item quantity updated."
else
    echo "   Error: Failed to update item quantity. Exiting."
    exit 1
fi
echo "-----------------------------------------"

# ----------------- 3. CHECK UPDATED STATUS (GET /api/cart/) -----------------
echo "3. GET: Verifying updated quantity in cart..."
RESPONSE=$(curl -s -X GET -b $COOKIE_FILE "$HOST/api/cart/")

# Check if the response contains the updated quantity (5)
if [[ $RESPONSE == *'"quantity":5'* ]] && [[ $RESPONSE == *'"product_id":1'* ]]; then
    echo "   Success: Cart contains product with updated quantity (${UPDATE_QUANTITY})."
else
    echo "   Error: Item found, but quantity is incorrect. Exiting."
    exit 1
fi
echo "-----------------------------------------"

# ----------------- 4. REMOVE ITEM (DELETE /api/cart/1/) -----------------
echo "4. DELETE: Removing item..."
DELETE_URL="$HOST/api/cart/$PRODUCT_ID/"
RESPONSE_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X DELETE -b $COOKIE_FILE "$DELETE_URL")

if [ "$RESPONSE_CODE" -eq 204 ] || [ "$RESPONSE_CODE" -eq 200 ]; then
    echo "   Success: Item removed (HTTP $RESPONSE_CODE)."
else
    echo "   Error: Deletion failed (HTTP $RESPONSE_CODE). Exiting."
    exit 1
fi
echo "-----------------------------------------"

# ----------------- 5. FINAL CHECK (GET) -----------------
echo "5. GET: Final check (cart should be empty)..."
RESPONSE=$(curl -s -X GET -b $COOKIE_FILE "$HOST/api/cart/")

if [[ $RESPONSE == *'"items":[]'* ]]; then
    echo "   Success: Cart is empty. All tests passed."
else
    echo "   Error: Cart is not empty after deletion. Exiting."
    exit 1
fi
echo "-----------------------------------------"
