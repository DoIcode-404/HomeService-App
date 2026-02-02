import 'package:client/data/constants/constants.dart';
import 'package:client/model/payment_model.dart';
import 'package:client/modules/payment/components/add_new_card_sheet.dart';
import 'package:client/modules/payment/components/payment_card.dart';
import 'package:client/modules/widgets/buttons/custom_button.dart';
import 'package:client/modules/widgets/containers/primary_container.dart';
import 'package:client/modules/widgets/texts/custom_header_text.dart';
import 'package:flutter/material.dart';

class PaymentMethodView extends StatefulWidget {
  const PaymentMethodView({super.key});

  @override
  State<PaymentMethodView> createState() => _PaymentMethodViewState();
}

class _PaymentMethodViewState extends State<PaymentMethodView> {
  int _selectedPayment = 0;
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(leading: const BackButton()),
      body: SingleChildScrollView(
        padding: EdgeInsets.symmetric(horizontal: 20),
        child: Column(
          children: [
            SizedBox(height: 20),
            PrimaryContainer(
              child: Column(
                children: [
                  Row(
                    children: [
                      CustomHeaderText(text: 'Add Card List', fontSize: 18),
                      const Spacer(),
                      CustomButton(
                        icon: AppAssets.kAddRounded,
                        onTap: () {
                          showModalBottomSheet(
                            context: context,
                            isScrollControlled: true,
                            builder: (context) {
                              return const AddNewCardSheet();
                            },
                          );
                        },
                        text: 'Add New',
                        isBorder: true,
                      ),
                    ],
                  ),
                  SizedBox(height: 16),
                  PrimaryContainer(
                    child: ListView.separated(
                      shrinkWrap: true,
                      physics: const NeverScrollableScrollPhysics(),
                      itemBuilder: (context, index) {
                        return PaymentCard(
                          payment: paymentMethods[index],
                          onTap: () {
                            setState(() {
                              _selectedPayment = index;
                            });
                          },
                          selectedPayment: _selectedPayment == index,
                        );
                      },
                      separatorBuilder: (context, index) => Divider(height: 20),
                      itemCount: paymentMethods.length,
                    ),
                  ),
                ],
              ),
            ),
            SizedBox(height: 16),
            PrimaryContainer(
              child: Column(
                children: [
                  CustomHeaderText(text: 'Your Credit', fontSize: 18),
                  SizedBox(height: 16),
                  PaymentCard(
                    onTap: () {},
                    titleColor: AppColors.kAccent1,
                    payment: PaymentModel(
                      id: '1',
                      cardNumber: r'USD 500',
                      expireDate: 'Exp 04/2023',
                      image: AppAssets.kMyCard,
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
