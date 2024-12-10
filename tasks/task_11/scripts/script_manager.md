## COMMON

```json
{
  "_id": UUID("..."),
  "type": "TYPE",   // Extraction, FieldRule, AnonymizationRule, Transformation, Uploading
  "released": false,
  "fields": [ 
    { "source": "ext_datamodule_id_1", "name": "fieldName1" },
    { "source": "ext_datamodule_id_2", "name": "fieldName2" }
  ],
  ...
}
```

## Field Rule
```json
{
    ...
    "fieldRuleType": "TYPE",     // FillEmpty, IgnoreEmpty, RemoveEmpty, FillOutOfRange, IgnoreOutOfRange, RemoveOutOfRange
    "defaultValue": {...},            
    "minValue": {...},                
    "maxValue": {...},                
    "fieldType": "string indicating type"
}
```

## Anonymization Rule

```json
{
    ...
    "anonymizationRuleType": "Type"   //  Generalization,  Suppression, Anatomization, Permutation, Pertubation

}
```

## Transformation

```json
{
    ...
    "transformationType": "Type",   //  Merge, Update
    "transformationScript": "string or null"
}
```

## Common scripts examples

### Get by id:

```js
const script = db.processing_scripts.findOne({_id: UUID("...")});
```

### Get by type:

```js
db.processing_scripts.find({type: "TransformationScript"});
```

### Get released:

```js
db.processing_scripts.find({released: true});
```
