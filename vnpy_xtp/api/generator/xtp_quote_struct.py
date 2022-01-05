XTPSpecificTickerStruct = {
	"exchange_id": "enum",
	"ticker": "char",
}

XTPMarketDataStockExData = {
	"total_bid_qty": "int64_t",
	"total_ask_qty": "int64_t",
	"ma_bid_price": "double",
	"ma_ask_price": "double",
	"ma_bond_bid_price": "double",
	"ma_bond_ask_price": "double",
	"yield_to_maturity": "double",
	"iopv": "double",
	"etf_buy_count": "int32_t",
	"etf_sell_count": "int32_t",
	"etf_buy_qty": "double",
	"etf_buy_money": "double",
	"etf_sell_qty": "double",
	"etf_sell_money": "double",
	"total_warrant_exec_qty": "double",
	"warrant_lower_price": "double",
	"warrant_upper_price": "double",
	"cancel_buy_count": "int32_t",
	"cancel_sell_count": "int32_t",
	"cancel_buy_qty": "double",
	"cancel_sell_qty": "double",
	"cancel_buy_money": "double",
	"cancel_sell_money": "double",
	"total_buy_count": "int64_t",
	"total_sell_count": "int64_t",
	"duration_after_buy": "int32_t",
	"duration_after_sell": "int32_t",
	"num_bid_orders": "int32_t",
	"num_ask_orders": "int32_t",
	"pre_iopv": "double",
	"r1": "int64_t",
	"r2": "int64_t",
}

XTPMarketDataOptionExData = {
	"auction_price": "double",
	"auction_qty": "int64_t",
	"last_enquiry_time": "int64_t",
}

XTPMarketDataStruct = {
	"exchange_id": "enum",
	"ticker": "char",
	"last_price": "double",
	"pre_close_price": "double",
	"open_price": "double",
	"high_price": "double",
	"low_price": "double",
	"close_price": "double",
	"pre_total_long_positon": "int64_t",
	"total_long_positon": "int64_t",
	"pre_settl_price": "double",
	"settl_price": "double",
	"upper_limit_price": "double",
	"lower_limit_price": "double",
	"pre_delta": "double",
	"curr_delta": "double",
	"data_time": "int64_t",
	"qty": "int64_t",
	"turnover": "double",
	"avg_price": "double",
	"bid": "double",
	"ask": "double",
	"bid_qty": "int64_t",
	"ask_qty": "int64_t",
	"trades_count": "int64_t",
	"ticker_status": "char",
	"stk": "XTPMarketDataStockExData",
	"opt": "XTPMarketDataOptionExData",
	"data_type": "XTP_MARKETDATA_TYPE",
	"r4": "int32_t",
}

XTPQuoteStaticInfo = {
	"exchange_id": "enum",
	"ticker": "char",
	"ticker_name": "char",
	"ticker_type": "enum",
	"pre_close_price": "double",
	"upper_limit_price": "double",
	"lower_limit_price": "double",
	"price_tick": "double",
	"buy_qty_unit": "int32_t",
	"sell_qty_unit": "int32_t",
}

OrderBookStruct = {
	"exchange_id": "enum",
	"ticker": "char",
	"last_price": "double",
	"qty": "int64_t",
	"turnover": "double",
	"trades_count": "int64_t",
	"bid": "double",
	"ask": "double",
	"bid_qty": "int64_t",
	"ask_qty": "int64_t",
	"data_time": "int64_t",
}

XTPTickByTickEntrust = {
	"channel_no": "int32_t",
	"seq": "int64_t",
	"price": "double",
	"qty": "int64_t",
	"side": "char",
	"ord_type": "char",
}

XTPTickByTickTrade = {
	"channel_no": "int32_t",
	"seq": "int64_t",
	"price": "double",
	"qty": "int64_t",
	"money": "double",
	"bid_no": "int64_t",
	"ask_no": "int64_t",
	"trade_flag": "char",
}

XTPTickByTickStruct = {
	"exchange_id": "enum",
	"ticker": "char",
	"seq": "int64_t",
	"data_time": "int64_t",
	"type": "enum",
	"entrust": "XTPTickByTickEntrust",
	"trade": "XTPTickByTickTrade",
}

XTPTickerPriceInfo = {
	"exchange_id": "enum",
	"ticker": "char",
	"last_price": "double",
}

XTPQuoteFullInfo = {
	"exchange_id": "enum",
	"ticker": "char",
	"ticker_name": "char",
	"security_type": "enum",
	"ticker_qualification_class": "enum",
	"is_registration": "bool",
	"is_VIE": "bool",
	"is_noprofit": "bool",
	"is_weighted_voting_rights": "bool",
	"is_have_price_limit": "bool",
	"upper_limit_price": "double",
	"lower_limit_price": "double",
	"pre_close_price": "double",
	"price_tick": "double",
	"bid_qty_upper_limit": "int32_t",
	"bid_qty_lower_limit": "int32_t",
	"bid_qty_unit": "int32_t",
	"ask_qty_upper_limit": "int32_t",
	"ask_qty_lower_limit": "int32_t",
	"ask_qty_unit": "int32_t",
	"market_bid_qty_upper_limit": "int32_t",
	"market_bid_qty_lower_limit": "int32_t",
	"market_bid_qty_unit": "int32_t",
	"market_ask_qty_upper_limit": "int32_t",
	"market_ask_qty_lower_limit": "int32_t",
	"market_ask_qty_unit": "int32_t",
	"unknown": "uint64_t",
}

