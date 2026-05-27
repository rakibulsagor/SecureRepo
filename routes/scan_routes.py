from flask import Blueprint, jsonify, request

from services.report_service import ReportService

scan_blueprint = Blueprint("scan", __name__)
report_service = ReportService()


@scan_blueprint.post("/api/scan")
def scan_repository():
    payload = request.get_json(silent=True) or {}
    repo_url = str(payload.get("repo_url", "")).strip()
    use_ai_explanation = bool(payload.get("use_ai_explanation", True))

    if not repo_url:
        return jsonify({"detail": "Repository URL or local path is required."}), 400

    try:
        report = report_service.generate_report(
            repo_url=repo_url,
            use_ai_explanation=use_ai_explanation,
        )
        return jsonify(report)
    except ValueError as exc:
        return jsonify({"detail": str(exc)}), 400
    except RuntimeError as exc:
        return jsonify({"detail": str(exc)}), 502
    except Exception as exc:
        return jsonify({"detail": f"Internal scanning error: {exc}"}), 500
