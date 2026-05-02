def create_order(user_id, product_id, quantity):
    """当前的下单流程（有问题）"""
    # 1. 检查库存
    stock = product_service.get_stock(product_id)
    if stock < quantity:
        raise Exception("库存不足")
    
    # 2. 扣减库存
    product_service.reduce_stock(product_id, quantity)
    
    # 3. 创建订单
    order = order_service.create_order(user_id, product_id, quantity)
    
    # 4. 发起支付
    payment_result = payment_service.create_payment(order['id'], order['amount'])
    
    # 5. 更新订单状态
    if payment_result['status'] == 'success':
        order_service.update_order_status(order['id'], 'paid')
        # 通知物流服务
        shipping_service.create_shipping(order['id'])
    else:
        # 恢复库存
        product_service.increase_stock(product_id, quantity)
        order_service.update_order_status(order['id'], 'failed')
    
    return order
