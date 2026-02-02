import 'package:client/data/constants/constants.dart';
import 'package:client/model/payment_model.dart';
import 'package:client/modules/widgets/buttons/custom_button.dart';
import 'package:flutter/material.dart';

class PaymentCard extends StatelessWidget {
  final PaymentModel payment;
  final VoidCallback onTap;
  final bool? selectedPayment;
  final Color? titleColor;
  const PaymentCard({
    super.key,
    required this.payment,
    required this.onTap,
    this.selectedPayment,
    this.titleColor,
  });

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      child: Row(
        children: [
          Container(
            height: 55,
            width: 55,
            alignment: Alignment.center,
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              image: DecorationImage(
                image: AssetImage(payment.image),
                fit: BoxFit.cover,
              ),
            ),
          ),
          SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  payment.cardNumber,
                  style: AppTypography.kMedium16.copyWith(color: titleColor),
                ),
                SizedBox(height: 5),
                Text(
                  payment.expireDate,
                  style: AppTypography.kLight13.copyWith(
                    color: AppColors.kNeutral,
                  ),
                ),
              ],
            ),
          ),
          selectedPayment != null
              ? Container(
                height: 20,
                width: 20,
                padding: EdgeInsets.all(2),
                decoration: BoxDecoration(
                  border: Border.all(color: AppColors.kPrimary, width: 2),
                  shape: BoxShape.circle,
                ),
                child:
                    selectedPayment!
                        ? Container(
                          decoration: const BoxDecoration(
                            color: AppColors.kPrimary,
                            shape: BoxShape.circle,
                          ),
                        )
                        : null,
              )
              : IgnorePointer(
                ignoring: true,
                child: CustomButton(
                  icon: AppAssets.kEdit,
                  onTap: () {},
                  text: 'Apply',
                  isBorder: true,
                ),
              ),
        ],
      ),
    );
  }
}
