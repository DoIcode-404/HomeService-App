import 'package:client/data/constants/app_assets.dart';
import 'package:client/model/address_model.dart';
import 'package:client/modules/address/components/address_card.dart';
import 'package:client/modules/widgets/buttons/custom_button.dart';
import 'package:client/modules/widgets/containers/primary_container.dart';
import 'package:client/modules/widgets/texts/custom_header_text.dart';
import 'package:flutter/material.dart';

import 'package:flutter_svg/flutter_svg.dart';

class AddressView extends StatefulWidget {
  final bool isCheckOutPage;
  const AddressView({super.key, this.isCheckOutPage = false});

  @override
  State<AddressView> createState() => _AddressViewState();
}

class _AddressViewState extends State<AddressView> {
  int _selectedAddress = 0;
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(leading: const BackButton()),
      body: SingleChildScrollView(
        padding: EdgeInsets.symmetric(horizontal: 20),
        child: Column(
          children: [
            widget.isCheckOutPage ? SizedBox(height: 20) : const SizedBox(),
            widget.isCheckOutPage
                ? PrimaryContainer(
                  child: Row(
                    children: [
                      CustomHeaderText(
                        text: 'At my Current Location',
                        fontSize: 18,
                      ),
                      const Spacer(),
                      SvgPicture.asset(AppAssets.kCurrentLocation),
                    ],
                  ),
                )
                : const SizedBox(),
            SizedBox(height: 20),
            Row(
              children: [
                const CustomHeaderText(text: 'Address'),
                const Spacer(),
                widget.isCheckOutPage
                    ? CustomButton(
                      onTap: () {},
                      icon: AppAssets.kAddRounded,
                      text: 'Add New',
                    )
                    : const SizedBox(),
              ],
            ),
            SizedBox(height: 20),
            PrimaryContainer(
              child: ListView.separated(
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                itemBuilder: (context, index) {
                  return AddressCard(
                    onTap: () {
                      setState(() {
                        _selectedAddress = index;
                      });
                    },
                    selectedAddress: _selectedAddress == index,
                    address: dummyAddresses[index],
                    isCheckOutPage: widget.isCheckOutPage,
                  );
                },
                separatorBuilder: (context, index) => Divider(height: 20),
                itemCount: dummyAddresses.length,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
