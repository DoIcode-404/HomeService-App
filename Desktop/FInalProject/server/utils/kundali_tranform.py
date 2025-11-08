# from server.pydantic_schemas.kundali_schema import KundaliResponse
# # from routes import kundali


# def transform_kundali_response(kundali: 'KundaliResponse') -> dict:
#     transformed = {}

#     # Access planet data from Pydantic model or dict
#     for planet, data in kundali.planets.items():
#         transformed[planet] = {
#             "sign": data.sign.strip(),
#             "house": data.house,
#             "degree": data.longitude
#         }

#     # Add Ascendant
#     transformed["Ascendant"] = {
#         "sign": kundali.ascendant.sign.strip(),
#         "house": 1,
#         "degree": kundali.ascendant.longitude
#     }

#     return transformed

