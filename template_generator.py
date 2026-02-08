"""
Template Generator Module
Generates COREP form extracts from LLM output
"""

def generate_corep_template(llm_response):
    """
    Takes the LLM JSON response and formats it as a COREP-like table
    
    Args:
        llm_response: JSON string from LLM
    
    Returns:
        HTML formatted table
    """
    
    try:
        import json
        data = json.loads(llm_response)
        
        # Build HTML table - using simple HTML for now
        
        
        html = """
        <div style='margin-top: 20px;'>
            <h3>📋 COREP Template Extract - Own Funds (C 01.00)</h3>
            <table style='width:100%; border-collapse: collapse; margin-top:15px;'>
                <thead style='background-color: #007bff; color: white;'>
                    <tr>
                        <th style='border: 1px solid #ddd; padding: 12px; text-align: left;'>Row</th>
                        <th style='border: 1px solid #ddd; padding: 12px; text-align: left;'>Field Name</th>
                        <th style='border: 1px solid #ddd; padding: 12px; text-align: right;'>Amount (£000)</th>
                        <th style='border: 1px solid #ddd; padding: 12px; text-align: left;'>Rule Reference</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        # Add rows from LLM response
        row_num = 10
        for field in data.get('required_fields', []):
            html += f"""
                <tr style='background-color: {"#f8f9fa" if row_num % 20 == 0 else "white"}'>
                    <td style='border: 1px solid #ddd; padding: 10px;'>{row_num:03d}</td>
                    <td style='border: 1px solid #ddd; padding: 10px;'>{field.get('field_name', 'N/A')}</td>
                    <td style='border: 1px solid #ddd; padding: 10px; text-align: right;'>{field.get('value', '-')}</td>
                    <td style='border: 1px solid #ddd; padding: 10px; font-size: 12px;'>{field.get('rule_reference', 'N/A')}</td>
                </tr>
            """
            row_num += 10
        
        html += """
                </tbody>
            </table>
        </div>
        """
        
        # Add audit trail section
        html += f"""
        <div style='margin-top: 20px; padding: 15px; background-color: #fff3cd; border-left: 4px solid #ffc107; border-radius: 5px;'>
            <h4 style='margin-top: 0;'>⚠️ Validation Notes:</h4>
            <p>{data.get('validation_notes', 'No validation issues detected')}</p>
        </div>
        
        <div style='margin-top: 20px; padding: 15px; background-color: #d1ecf1; border-left: 4px solid #17a2b8; border-radius: 5px;'>
            <h4 style='margin-top: 0;'>📝 Audit Trail:</h4>
            <p style='font-size: 14px;'>{data.get('audit_trail', 'No audit information available')}</p>
            <p style='font-size: 12px; margin-top: 10px;'><strong>Rules Applied:</strong> {', '.join(data.get('applicable_rules', ['None']))}</p>
        </div>
        """
        
        return html
        
    except Exception as e:
        return f"<p style='color: red;'>Error generating template: {str(e)}</p>"


def validate_fields(fields):
    """
    Basic validation rules for COREP fields
    
    """
    errors = []
    
    for field in fields:
        field_name = field.get('field_name', '')
        value = field.get('value', '')
        
        # Check if value is numeric where expected
        if value and value != '-':
            try:
                num_val = float(value.replace(',', '').replace('£', '').replace('M', ''))
                
                # Basic business rules
                if 'deduction' in field_name.lower() and num_val > 0:
                    errors.append(f"Warning: {field_name} should typically be negative (deduction)")
                
                if 'capital' in field_name.lower() and num_val < 0:
                    errors.append(f"Warning: {field_name} is negative - please verify")
                    
            except ValueError:
                errors.append(f"Error: {field_name} has non-numeric value: {value}")
    
    return errors