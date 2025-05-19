# 🧪 Data Quality Report
Generated on: 2025-05-19T09:20:26.523872

Threshold: 5

**Total Issues:** 4

**Severity Points:** 12

**Status:** fail

---

### ❌ range_check — age
- **Error**: max_value
- **Severity**: medium (3)
- **Actual Value**: `200`
- **Timestamp**: 2025-05-19 09:20:26.481709

---

### ❌ range_check — height
- **Error**: max_value
- **Severity**: medium (3)
- **Actual Value**: `11.0`
- **Timestamp**: 2025-05-19 09:20:26.482710

---

### ❌ regex_check — ip_address
- **Error**: regex_mismatch
- **Severity**: low (1)
- **Actual Value**: `2    252/30.214-249
Name: ip_address, dtype: object`
- **Timestamp**: 2025-05-19 09:20:26.486709

---

### ❌ null_check — email
- **Error**: null_value
- **Severity**: high (5)
- **Actual Value**: `4    NaN
5    NaN
6    NaN
Name: email, dtype: object`
- **Timestamp**: 2025-05-19 09:20:26.486709

---

