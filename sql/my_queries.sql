drop table if exists f1;
create table if not exists f1(
    id integer primary key autoincrement not null,
    intent text not null,
    requests integer not null
);

insert into f1 (intent, requests)
select interaction.intent, count(interaction.intent)
from interaction
group by intent;


drop table if exists f2;
create table if not exists f2(
    id integer primary key autoincrement not null,
    intent text not null,
    latency_ms float not null
);

insert into f2 (intent, latency_ms)
select interaction.intent, round(avg(interaction.latency_ms), 2)
from interaction
group by intent;


drop table if exists f3;
create table if not exists f3(
    id integer primary key autoincrement not null,
    topic text not null,
    thumbs_down float not null
);

insert into f3 (topic, thumbs_down)
select topic, count(rating) 
from interaction
inner join feedback
    on interaction.request_id = feedback.request_id
where topic is not null
group by topic;


drop table if exists h2;
create table if not exists h2(
    id integer primary key autoincrement not null,
    intent text not null,
    worst_latency float,
    best_latency float,
    total_requests integer,
    resolve_pct float,
    degraded_pct float
);

-- Analytic question: What are the status across all intent and percentage of degraded and resolved of each intent? ---
insert into h2 (intent, worst_latency, best_latency, total_requests, resolve_pct, degraded_pct)
select intent, 
       max(latency_ms), 
       min(latency_ms), 
       count(id), 
       round((sum(case when resolved then 1 else 0 end) * 100.0) / count(id), 2), 
       round((sum(case when degraded then 1 else 0 end) * 100.0) / count(id), 2)
from interaction
group by intent;
