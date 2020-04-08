from alipay import AliPay
from urllib.request import urlopen


class AliAppPayment:
    """
    支付宝app支付功能
    """
    def __init__(self):
        self.app_private_key_string = open("./private_key.txt").read()
        self.ali_public_key_string = open("./public_key.txt").read()
        self.alipay = AliPay(
            appid="2019042664373131",  # 商户appid
            app_notify_url=None,  # 默认回调url
            # 支付宝私钥
            app_private_key_string=self.app_private_key_string,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=self.ali_public_key_string,
            sign_type="RSA2",
            debug=False
        )

    def get_order_string(self, out_trade_no, t_amount, subject):
        order_string = self.alipay.api_alipay_trade_app_pay(
            out_trade_no=str(out_trade_no),
            total_amount=str(t_amount),
            subject=subject,
            # 部署时，修改该url为http+本机外网ip或域名
            # notify_url="http://106.14.127.164:8080/amount/deposit/return"
            notify_url="http://106.14.127.164:5000/pay/alipayment_notify"
        )
        return order_string


class AliAgreementSign(AliPay):
    """
    用于订阅签约SDK
    """
    def alipay_user_subscribe(self, personal_product_code, external_agreement_no, period_type, period, execute_time,
                              single_amount, total_amount=None, total_payments=None, sign_validity_period=None):
        biz_content = {
            "personal_product_code": personal_product_code,
            "external_agreement_no": external_agreement_no,
            "period_rule_params": {
                "period_type": period_type,
                "period": period,
                "execute_time": execute_time,
                "single_amount": single_amount
            }
        }
        if sign_validity_period:
            biz_content["sign_validity_period"] = sign_validity_period
        if total_amount:
            biz_content["period_rule_params"]["total_amount"] = total_amount
        if total_payments:
            biz_content["period_rule_params"]["total_payments"] = total_payments

        data = self.build_body(
            "alipay.user.agreement.page.sign",
            biz_content,
            append_auth_token=False
        )
        url = self._gateway + "?" + self.sign_data(data)
        raw_string = urlopen(url, timeout=15).read().decode("utf-8")
        return self._verify_and_return_sync_response(
            raw_string, "alipay_user_agreement_page_sign_response"
        )


class AliAgreementSignment:
    """
    支付宝用户订阅功能
    """
    def __init__(self):
        self.app_private_key_string = open("./private_key.txt").read()
        self.ali_public_key_string = open("./public_key.txt").read()
        self.alipay = AliAgreementSign(
            appid="2019042664373131",
            app_notify_url=None,  # 默认回调url
            # 支付宝私钥
            app_private_key_string=self.app_private_key_string,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=self.ali_public_key_string,
            sign_type="RSA2",
            debug=False
        )

    def sign_user_agreement(self, external_agreement_no, personal_product_code, period_type, period, execute_time,
                            single_amount, total_amount=None, total_payments=None, sign_validity_period=None):
        """

        :param external_agreement_no: 商户签约号
        :param personal_product_code: 个人签约产品码，商户和支付宝签约时确定
        :param period_type: 周期类型：DAY/MONTH，若扣款周期为90天，period_type=DAY
        :param period: 周期数，若扣款周期为90天，period=90
        :param execute_time: 首次扣款时间
        :param single_amount: 单笔最大金额
        :param total_amount: 总金额
        :param total_payments: 总扣款次数
        :param sign_validity_period: 当前用户签约请求的协议有效周期（日d/月m），不填则长期有效。
                                    整形数字加上时间单位的协议有效期，从发起签约请求的时间开始算起。
        :return:
        """
        response = self.alipay.alipay_user_subscribe(
            external_agreement_no=str(external_agreement_no),
            personal_product_code=personal_product_code,
            period_type=period_type,
            period=period,
            execute_time=execute_time,
            single_amount=single_amount,
            total_amount=total_amount,
            total_payments=total_payments,
            sign_validity_period=sign_validity_period
        )
        if response["code"] == "10000":
            return True
        else:
            return False
