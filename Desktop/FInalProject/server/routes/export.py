"""
Export Routes
Handles Kundali export to various formats (CSV, JSON, PDF).

All responses follow standardized APIResponse format.

Author: Backend API Team
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import logging
from typing import List
import time

from server.pydantic_schemas.kundali_schema import KundaliRequest
from server.pydantic_schemas.api_response import APIResponse, success_response, error_response
from server.services.logic import generate_kundali_logic
from server.ml.exporter import KundaliMLExporter, export_training_data

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post('/kundali-csv', response_model=APIResponse, tags=["Export"])
async def export_kundali_csv(request: KundaliRequest) -> APIResponse:
    """
    Generate Kundali and export to CSV format.

    Args:
        request: Birth details for Kundali generation

    Returns:
        APIResponse with CSV file URL or attachment
    """
    try:
        logger.info(f"Exporting Kundali to CSV for: {request.birthDate}")

        # Generate kundali
        kundali_response = await generate_kundali_logic(request)

        # Export to CSV
        exporter = KundaliMLExporter()
        filename = f"kundali_{request.birthDate.replace('-', '')}.csv"
        csv_data = exporter.to_csv([kundali_response], filename)

        logger.info(f"CSV export successful: {filename}")

        # Return file or data based on your needs
        return success_response(
            data={
                "format": "csv",
                "filename": filename,
                "message": "CSV export generated"
            },
            message="Kundali exported to CSV successfully"
        )

    except Exception as e:
        logger.error(f"CSV export failed: {str(e)}", exc_info=True)
        response, status_code = error_response(
            code="EXPORT_CSV_ERROR",
            message=str(e),
            http_status=500
        )
        raise HTTPException(status_code=status_code, detail=response.error.message)


@router.post('/kundali-json', response_model=APIResponse, tags=["Export"])
async def export_kundali_json(request: KundaliRequest) -> APIResponse:
    """
    Generate Kundali and export to JSON format.

    Args:
        request: Birth details for Kundali generation

    Returns:
        APIResponse with JSON data
    """
    try:
        logger.info(f"Exporting Kundali to JSON for: {request.birthDate}")

        # Generate kundali
        kundali_response = await generate_kundali_logic(request)

        # Export to JSON
        filename = f"kundali_{request.birthDate.replace('-', '')}.json"
        export_training_data([kundali_response], filename)

        logger.info(f"JSON export successful: {filename}")

        return success_response(
            data={
                "format": "json",
                "filename": filename,
                "kundali": kundali_response.model_dump(exclude_none=True)
            },
            message="Kundali exported to JSON successfully"
        )

    except Exception as e:
        logger.error(f"JSON export failed: {str(e)}", exc_info=True)
        response, status_code = error_response(
            code="EXPORT_JSON_ERROR",
            message=str(e),
            http_status=500
        )
        raise HTTPException(status_code=status_code, detail=response.error.message)


@router.post('/batch-kundali-csv', response_model=APIResponse, tags=["Export"])
async def export_batch_kundali_csv(requests: List[KundaliRequest]) -> APIResponse:
    """
    Generate multiple Kundalis and export to CSV format.

    Useful for batch processing and comparative analysis.

    Args:
        requests: List of birth details for multiple Kundalis

    Returns:
        APIResponse with batch CSV export information
    """
    try:
        start_time = time.time()
        logger.info(f"Batch exporting {len(requests)} Kundalis to CSV")

        kundali_responses = []
        successful = 0
        failed = 0

        for i, request in enumerate(requests):
            try:
                kundali_response = await generate_kundali_logic(request)
                kundali_responses.append(kundali_response)
                successful += 1
            except Exception as e:
                logger.warning(f"Failed to generate Kundali {i+1}: {str(e)}")
                failed += 1

        if not kundali_responses:
            response, status_code = error_response(
                code="NO_RECORDS_GENERATED",
                message="Failed to generate any Kundalis",
                http_status=400
            )
            raise HTTPException(status_code=status_code, detail=response.error.message)

        # Export to CSV
        exporter = KundaliMLExporter()
        filename = f"batch_kundali_{successful}_records.csv"
        csv_data = exporter.to_csv(kundali_responses, filename)

        calculation_time = (time.time() - start_time) * 1000

        logger.info(f"Batch CSV export successful: {filename} ({successful} records in {calculation_time:.2f}ms)")

        return success_response(
            data={
                "format": "csv",
                "filename": filename,
                "total_requested": len(requests),
                "successful": successful,
                "failed": failed,
                "time_ms": calculation_time
            },
            message=f"Batch export completed: {successful}/{len(requests)} Kundalis exported"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Batch CSV export failed: {str(e)}", exc_info=True)
        response, status_code = error_response(
            code="BATCH_EXPORT_ERROR",
            message=str(e),
            http_status=500
        )
        raise HTTPException(status_code=status_code, detail=response.error.message)


@router.post('/batch-kundali-json', response_model=APIResponse, tags=["Export"])
async def export_batch_kundali_json(requests: List[KundaliRequest]) -> APIResponse:
    """
    Generate multiple Kundalis and export to JSON format.

    Useful for data synchronization and API integrations.

    Args:
        requests: List of birth details for multiple Kundalis

    Returns:
        APIResponse with batch JSON export data
    """
    try:
        start_time = time.time()
        logger.info(f"Batch exporting {len(requests)} Kundalis to JSON")

        kundali_responses = []
        successful = 0
        failed = 0

        for i, request in enumerate(requests):
            try:
                kundali_response = await generate_kundali_logic(request)
                kundali_responses.append(kundali_response)
                successful += 1
            except Exception as e:
                logger.warning(f"Failed to generate Kundali {i+1}: {str(e)}")
                failed += 1

        if not kundali_responses:
            response, status_code = error_response(
                code="NO_RECORDS_GENERATED",
                message="Failed to generate any Kundalis",
                http_status=400
            )
            raise HTTPException(status_code=status_code, detail=response.error.message)

        # Export to JSON
        filename = f"batch_kundali_{successful}_records.json"
        export_training_data(kundali_responses, filename)

        calculation_time = (time.time() - start_time) * 1000

        logger.info(f"Batch JSON export successful: {filename} ({successful} records in {calculation_time:.2f}ms)")

        return success_response(
            data={
                "format": "json",
                "filename": filename,
                "total_requested": len(requests),
                "successful": successful,
                "failed": failed,
                "kundalis": [k.model_dump(exclude_none=True) for k in kundali_responses],
                "time_ms": calculation_time
            },
            message=f"Batch export completed: {successful}/{len(requests)} Kundalis exported"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Batch JSON export failed: {str(e)}", exc_info=True)
        response, status_code = error_response(
            code="BATCH_EXPORT_ERROR",
            message=str(e),
            http_status=500
        )
        raise HTTPException(status_code=status_code, detail=response.error.message)