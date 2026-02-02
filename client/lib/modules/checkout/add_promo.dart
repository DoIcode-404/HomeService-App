import 'package:client/modules/checkout/components/promo_card.dart';
import 'package:client/modules/home/components/search_field.dart';
import 'package:client/modules/widgets/containers/primary_container.dart';
import 'package:client/modules/widgets/texts/custom_header_text.dart';
import 'package:flutter/material.dart';

class AddPromoCode extends StatefulWidget {
  const AddPromoCode({super.key});

  @override
  State<AddPromoCode> createState() => _AddPromoCodeState();
}

class _AddPromoCodeState extends State<AddPromoCode> {
  final _promoCodeController = TextEditingController();
  int _selectedPromoCode = 0;
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
                  CustomHeaderText(text: 'Promo Code', fontSize: 18),
                  SizedBox(height: 16),
                  SearchField(
                    controller: _promoCodeController,
                    hintText: 'Apply Code',
                    buttonText: 'Apply',
                    isSearchField: false,
                    onSearchPress: () {},
                  ),
                ],
              ),
            ),
            SizedBox(height: 20),
            PrimaryContainer(
              child: Column(
                children: [
                  CustomHeaderText(text: 'Promo Code', fontSize: 18),
                  SizedBox(height: 16),
                  ListView.separated(
                    shrinkWrap: true,
                    physics: const NeverScrollableScrollPhysics(),
                    itemBuilder: (context, index) {
                      return PromoCard(
                        onTap: () {
                          setState(() {
                            _selectedPromoCode = index;
                          });
                        },
                        isSelected: _selectedPromoCode == index,
                      );
                    },
                    separatorBuilder: (context, index) => Divider(height: 20),
                    itemCount: 2,
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
