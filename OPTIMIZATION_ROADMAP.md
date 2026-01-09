# OwlPlanner Backend Optimization Roadmap

## Current State
**Weighted Scoring Model** + DFS schedule generation with in-memory CSV caching.

---

## Tier 1: Quick Wins (1-2 hours each)
Easy to implement, high impact, no major architecture changes.

### 1. Result Pagination & Top-N Limiting
**Problem:** Returning 1000+ schedules is wasteful; most users only view top 5-10.
**Solution:**
- Return only top 50 schedules by default
- Add `?limit=N&offset=M` query params for pagination
- Reduces memory/bandwidth, faster API response

**Complexity:** Low | **Value:** High

```python
@router.post("/schedules")
def generate_schedules(req: ScheduleRequest, limit: int = 50, offset: int = 0):
    all_schedules = generate_schedule(...)
    scored = sorted(all_schedules, key=score_schedule, reverse=True)
    return {
        "total": len(scored),
        "returned": len(scored[offset:offset+limit]),
        "limit": limit,
        "offset": offset,
        "schedules": scored[offset:offset+limit]
    }
```

### 2. Schedule Memoization
**Problem:** Same course combinations requested multiple times = re-generate same schedules.
**Solution:** Cache results by course set hash for 1 hour.
**Tools:** Python `functools.lru_cache` or simple dict with TTL

**Complexity:** Low | **Value:** Medium (only if users repeat searches)

### 3. Input Validation & Early Pruning
**Problem:** "Generate 1000 sections × 1000 sections × 1000 sections" → timeout/memory crash.
**Solution:**
- Limit: max 5 courses per request
- Validate each course exists before processing
- Return 400 error immediately for invalid input

**Complexity:** Low | **Value:** Medium (prevents abuse)

### 4. Conflict Detection Optimization
**Problem:** DFS checks all combinations; could short-circuit faster.
**Solution:**
- Precompute which sections conflict with each other (e.g., build conflict graph)
- Use graph coloring instead of brute-force DFS
- Reduces schedule generation time for large inputs

**Complexity:** Medium | **Value:** High (faster responses)

---

## Tier 2: Medium-Effort Enhancements (3-6 hours each)
Require architecture changes but significant benefits.

### 5. Database Layer (PostgreSQL)
**Problem:** CSV in-memory cache doesn't scale; no indexing; data refresh requires reload.
**Solution:**
- Migrate `course_data.csv` → PostgreSQL
- Index by course name, subject, CRN
- Query only what you need (filtered courses) instead of loading all 631

**Tech:** SQLAlchemy ORM + PostgreSQL
**Complexity:** Medium | **Value:** High (scalability, flexibility)

**Example benefit:** `SELECT * FROM courses WHERE course LIKE 'COMP%'` is faster than scanning 631 in-memory dicts.

### 6. Async/Concurrent Processing
**Problem:** Generating 100+ schedules is CPU-bound; single-threaded FastAPI blocks.
**Solution:**
- Use `asyncio` + `concurrent.futures` to generate schedules in parallel
- Split course list into partitions, process independently, merge results

**Complexity:** Medium | **Value:** Medium (only if many users hitting endpoint simultaneously)

### 7. Redis Caching Layer
**Problem:** Same searches repeat; API calls to /docs test repeatedly.
**Solution:**
- Cache POST /api/schedules responses by course set hash
- TTL 24 hours (invalidate at next scrape)
- Reduces computation for popular searches

**Tech:** Redis + `aioredis`
**Complexity:** Medium | **Value:** Medium (high-traffic scenarios)

### 8. Soft Constraints with Penalty Tuning
**Problem:** Weighted model works, but weights are hardcoded; users can't customize.
**Solution:**
- Create `POST /api/preferences` to accept custom weights
- Store in session/request context
- Pass to `score_schedule(schedule, weights)` as parameter
- Let users rerank same result set without regenerating

**Complexity:** Low-Medium | **Value:** High (user customization)

---

## Tier 3: Advanced Topics (8-20 hours each)
Significant learning curve, powerful results.

### 9. Integer Linear Programming (ILP)
**Problem:** Weighted model is heuristic; ILP finds globally optimal solution.
**Solution:**
- Use `pulp` or `ortools` to model as constraint satisfaction problem
- Define hard constraints: no time conflicts, max 2-hour gaps
- Minimize: early classes + schedule fragmentation
- Get provably optimal schedule per constraint set

**Tech:** Google OR-Tools or PuLP
**Complexity:** High (requires learning optimization theory) | **Value:** High (learning + portfolio)

**Example:**
```python
from ortools.linear_solver import pywraplp

# For each section, binary variable: selected=1 or not=0
# Constraint: sum of overlapping sections ≤ 1 (no conflicts)
# Minimize: 20*early_morning + 5*gaps - 30*compact
# Solve for optimal selection
```

### 10. Constraint Propagation & Pruning
**Problem:** DFS explores many invalid branches before detecting conflicts.
**Solution:**
- Use constraint propagation to eliminate impossible sections early
- Example: If COMP 140 section A is on Tue, eliminate MATH 212 sections also on Tue immediately
- Reduces search space dramatically

**Tech:** Constraint satisfaction problem (CSP) library (e.g., `python-constraint`)
**Complexity:** High | **Value:** Very High (exponential speedup for hard problems)

### 11. Multi-Objective Optimization (Pareto Front)
**Problem:** One user wants early classes, another wants compact schedules—single ranking doesn't satisfy both.
**Solution:**
- Generate Pareto-optimal schedules (non-dominated solutions)
- Return 2D visualization: compactness vs. early-ness
- User picks which tradeoff they prefer

**Tech:** Multi-objective optimization libraries
**Complexity:** Very High | **Value:** High (sophisticated UX)

---

## Tier 4: Infrastructure (10-40 hours)
Production-grade reliability.

### 12. Async Job Queue
**Problem:** Generating 500+ schedules takes 10+ seconds; user waits.
**Solution:**
- Receive request, queue computation job, return job ID immediately
- User polls `/api/jobs/{id}` for status
- Return results when ready
- Better UX for long-running tasks

**Tech:** Celery + Redis or AWS SQS
**Complexity:** Very High | **Value:** Medium (only needed at scale)

### 13. Metrics & Monitoring
**Problem:** Don't know if API is slow, which endpoints are popular, where bugs hide.
**Solution:**
- Add Prometheus metrics (request latency, cache hits, error rates)
- Deploy Grafana dashboard
- Alert on high latency or error spikes

**Tech:** Prometheus + Grafana
**Complexity:** Medium | **Value:** High (observability)

### 14. API Rate Limiting
**Problem:** One user/bot hammers API → DoS.
**Solution:**
- Rate limit by IP/API key (e.g., 10 requests/minute per IP)
- Return 429 if exceeded

**Tech:** `slowapi` (FastAPI extension)
**Complexity:** Low | **Value:** Medium (security)

---

## Recommended Implementation Order

### **This Week (Immediate)**
1. ✅ Weighted scoring model (DONE)
2. ⭐ Top-N limiting (1 hour) → Immediate UX improvement
3. ⭐ Input validation (30 mins) → Prevent crashes
4. Input: Custom preference weights (2 hours) → User customization

### **Next Week (Phase 2)**
5. Conflict detection optimization (3 hours) → Faster responses
6. Database migration to PostgreSQL (4 hours) → Scalability
7. ILP learning + basic implementation (6-8 hours) → Portfolio project

### **Following Week (Phase 3)**
8. Async processing (2-3 hours) → Concurrent requests
9. Redis caching (2 hours) → High-traffic optimization
10. Metrics/monitoring (2-3 hours) → Production readiness

### **Nice-to-Have (Lower Priority)**
11. Constraint propagation (8-12 hours) → Only if performance becomes bottleneck
12. Pareto front multi-objective (12-16 hours) → Advanced feature
13. Async job queue (8-10 hours) → Only if supporting 100+ concurrent users

---

## Technology Choices by Goal

| Goal | Tech | Effort | ROI |
|------|------|--------|-----|
| Speed up generation | Conflict graph + pruning | Medium | High |
| Scale to many users | PostgreSQL + Redis | High | High |
| Optimize solution quality | ILP (OR-Tools) | High | Very High |
| Enable personalization | Preference API | Low | High |
| Handle long jobs | Celery + Redis | Very High | Medium |
| Monitor health | Prometheus | Medium | High |

---

## My Recommendation for Your Timeline

**Today/Tomorrow:** Top-N limiting + validation (quick wins)
**Next 3 days:** Custom preferences endpoint (enables user research)
**Next week:** Start ILP learning (great learning project)
**Week 2:** PostgreSQL migration (scalability insurance)
**Week 3+:** Advanced optimizations based on actual usage patterns

This balances shipping features fast, learning new concepts, and maintaining code quality.

---

## Questions to Guide Your Choice

- **"Is generation slow?"** → Conflict detection optimization
- **"Do users want customization?"** → Preference weights endpoint
- **"Will this scale to 100+ users?"** → PostgreSQL + caching
- **"Want impressive portfolio project?"** → ILP implementation
- **"Do same searches repeat?"** → Redis caching
- **"Need production reliability?"** → Monitoring + rate limiting
